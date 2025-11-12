using System;
using System.Collections.Generic;
using System.IO;
using ClosedXML.Excel;
using NPOI.SS.UserModel;
using NPOI.XSSF.UserModel;
using NPOI.HSSF.UserModel;
using GaSongJang.Models;

namespace GaSongJang.Core;

/// <summary>
/// Excel 파일 처리 클래스 (XLS, XLSX 모두 지원)
/// 주문 데이터를 읽고 송장번호를 추가하여 저장
/// </summary>
public class ExcelProcessor
{
    /// <summary>
    /// Excel 파일에서 주문 데이터 읽기 (XLS, XLSX 모두 지원)
    /// </summary>
    public List<OrderData> ReadExcelFile(string filePath)
    {
        var orders = new List<OrderData>();

        try
        {
            IWorkbook workbook;

            // XLS 또는 XLSX 파일인지 판단하여 적절한 workbook 생성
            using (var fileStream = new FileStream(filePath, FileMode.Open, FileAccess.Read))
            {
                if (filePath.EndsWith(".xls", StringComparison.OrdinalIgnoreCase))
                {
                    workbook = new HSSFWorkbook(fileStream); // XLS (Excel 97-2003)
                }
                else if (filePath.EndsWith(".xlsx", StringComparison.OrdinalIgnoreCase))
                {
                    workbook = new XSSFWorkbook(fileStream); // XLSX (Excel 2007+)
                }
                else
                {
                    throw new Exception("지원되지 않는 파일 형식입니다. (XLS 또는 XLSX만 지원)");
                }

                var worksheet = workbook.GetSheetAt(0); // 첫 번째 시트 가져오기

                if (worksheet == null)
                    throw new Exception("Excel 파일에 시트가 없습니다.");

                int startRowIndex = 0;
                int rowCount = worksheet.PhysicalNumberOfRows;

                // 첫 행이 헤더인지 확인
                if (rowCount > 0)
                {
                    var firstRow = worksheet.GetRow(0);
                    if (firstRow != null && firstRow.PhysicalNumberOfCells >= 2)
                    {
                        var firstCellValue = firstRow.GetCell(0)?.StringCellValue ?? "";

                        if (firstCellValue.Contains("주문") || firstCellValue.Contains("코드") ||
                            firstCellValue.Contains("번호") || firstCellValue.Contains("마켓") ||
                            firstCellValue.Contains("이름") || !char.IsDigit(firstCellValue.FirstOrDefault()))
                        {
                            startRowIndex = 1; // 헤더 건너뛰기
                        }
                    }
                }

                // 데이터 행 처리
                for (int i = startRowIndex; i < rowCount; i++)
                {
                    try
                    {
                        var row = worksheet.GetRow(i);
                        if (row == null) continue;

                        var orderIDCell = row.GetCell(0);
                        var marketNameCell = row.GetCell(1);

                        if (orderIDCell == null || marketNameCell == null)
                            continue;

                        string orderID = orderIDCell.StringCellValue?.Trim() ?? "";
                        string marketName = marketNameCell.StringCellValue?.Trim() ?? "";

                        if (string.IsNullOrEmpty(orderID) || string.IsNullOrEmpty(marketName))
                            continue;

                        var order = new OrderData
                        {
                            OrderID = orderID,
                            MarketName = marketName
                        };

                        order.SetDeliveryCompany();
                        orders.Add(order);
                    }
                    catch
                    {
                        continue;
                    }
                }

                workbook.Close();
            }
        }
        catch (Exception ex)
        {
            throw new Exception($"Excel 파일 읽기 실패: {ex.Message}", ex);
        }

        if (orders.Count == 0)
            throw new Exception("Excel 파일에 유효한 데이터를 찾을 수 없습니다. (최소 2개 열 필요: 주문코드, 마켓이름)");

        return orders;
    }

    /// <summary>
    /// 송장번호가 포함된 데이터를 Excel 파일로 저장
    /// 출력 형식: 주문고유코드, 송장번호, 택배사 (3열)
    /// </summary>
    public void WriteExcelFile(List<OrderData> orders, string filePath)
    {
        try
        {
            using var workbook = new XLWorkbook();
            var worksheet = workbook.Worksheets.Add("송장생성결과");

            // 헤더 행
            worksheet.Cell(1, 1).Value = "주문고유코드";
            worksheet.Cell(1, 2).Value = "송장번호";
            worksheet.Cell(1, 3).Value = "택배사";

            // 헤더 스타일
            var headerRow = worksheet.Row(1);
            headerRow.Style.Font.Bold = true;
            headerRow.Style.Fill.BackgroundColor = XLColor.LightGray;

            // 데이터 행
            for (int i = 0; i < orders.Count; i++)
            {
                int rowNum = i + 2;
                var order = orders[i];

                worksheet.Cell(rowNum, 1).Value = order.OrderID;
                worksheet.Cell(rowNum, 2).Value = order.TrackingNumber;
                worksheet.Cell(rowNum, 3).Value = order.DeliveryCompany;
            }

            // 열 너비 자동 조정
            worksheet.Columns().AdjustToContents();

            // 파일 저장
            workbook.SaveAs(filePath);
        }
        catch (Exception ex)
        {
            throw new Exception($"Excel 파일 저장 실패: {ex.Message}", ex);
        }
    }
}
