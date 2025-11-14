using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
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
    /// Excel/CSV 파일에서 주문 데이터 읽기 (XLS, XLSX, CSV 모두 지원)
    /// 파일 구조: 주문번호, 주문고유코드, 마켓
    /// </summary>
    public List<OrderData> ReadExcelFile(string filePath)
    {
        if (filePath.EndsWith(".csv", StringComparison.OrdinalIgnoreCase))
        {
            return ReadCsvFile(filePath);
        }
        else
        {
            return ReadExcelNpoiFile(filePath);
        }
    }

    /// <summary>
    /// CSV 파일에서 주문 데이터 읽기
    /// </summary>
    private List<OrderData> ReadCsvFile(string filePath)
    {
        var orders = new List<OrderData>();

        try
        {
            var lines = File.ReadAllLines(filePath, Encoding.UTF8);

            int startIndex = 0;

            // 첫 행이 헤더인지 확인
            if (lines.Length > 0)
            {
                var firstLineParts = lines[0].Split('\t', ',');
                if (firstLineParts.Length >= 3 && !string.IsNullOrWhiteSpace(firstLineParts[2]))
                {
                    string firstMarket = firstLineParts[2].Trim();
                    if (!char.IsDigit(firstMarket[0]))
                    {
                        startIndex = 1; // 헤더 건너뛰기
                    }
                }
            }

            for (int i = startIndex; i < lines.Length; i++)
            {
                try
                {
                    var parts = lines[i].Split('\t', ',');

                    if (parts.Length < 3)
                        continue;

                    string orderID = parts[0]?.Trim() ?? "";
                    string orderCode = parts[1]?.Trim() ?? "";
                    string market = parts[2]?.Trim() ?? "";

                    if (string.IsNullOrEmpty(market))
                        continue;

                    var order = new OrderData
                    {
                        OrderID = orderID,
                        OrderCode = orderCode,
                        Market = market
                    };

                    order.SetDeliveryCompany();
                    orders.Add(order);
                }
                catch
                {
                    continue;
                }
            }
        }
        catch (Exception ex)
        {
            throw new Exception($"CSV 파일 읽기 실패: {ex.Message}", ex);
        }

        if (orders.Count == 0)
            throw new Exception("파일에 유효한 데이터를 찾을 수 없습니다. (최소 3개 열 필요: 주문번호, 주문고유코드, 마켓)");

        return orders;
    }

    /// <summary>
    /// Excel (XLS, XLSX) 파일에서 주문 데이터 읽기 (NPOI)
    /// </summary>
    private List<OrderData> ReadExcelNpoiFile(string filePath)
    {
        var orders = new List<OrderData>();

        try
        {
            IWorkbook workbook;

            using (var fileStream = new FileStream(filePath, FileMode.Open, FileAccess.Read))
            {
                if (filePath.EndsWith(".xls", StringComparison.OrdinalIgnoreCase))
                {
                    workbook = new HSSFWorkbook(fileStream);
                }
                else if (filePath.EndsWith(".xlsx", StringComparison.OrdinalIgnoreCase))
                {
                    workbook = new XSSFWorkbook(fileStream);
                }
                else
                {
                    throw new Exception("지원되지 않는 파일 형식입니다. (XLS, XLSX, CSV 지원)");
                }

                var worksheet = workbook.GetSheetAt(0);

                if (worksheet == null)
                    throw new Exception("Excel 파일에 시트가 없습니다.");

                int startRowIndex = 0;
                int rowCount = worksheet.PhysicalNumberOfRows;

                // 첫 행이 헤더인지 확인
                if (rowCount > 0)
                {
                    var firstRow = worksheet.GetRow(0);
                    if (firstRow != null && firstRow.PhysicalNumberOfCells >= 3)
                    {
                        var thirdCell = firstRow.GetCell(2);
                        string thirdCellValue = GetCellValueAsString(thirdCell);

                        if (!string.IsNullOrEmpty(thirdCellValue) && !char.IsDigit(thirdCellValue[0]))
                        {
                            startRowIndex = 1;
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
                        var orderCodeCell = row.GetCell(1);
                        var marketCell = row.GetCell(2);

                        if (marketCell == null)
                            continue;

                        string orderID = GetCellValueAsString(orderIDCell)?.Trim() ?? "";
                        string orderCode = GetCellValueAsString(orderCodeCell)?.Trim() ?? "";
                        string market = GetCellValueAsString(marketCell)?.Trim() ?? "";

                        if (string.IsNullOrEmpty(market))
                            continue;

                        var order = new OrderData
                        {
                            OrderID = orderID,
                            OrderCode = orderCode,
                            Market = market
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
            throw new Exception("파일에 유효한 데이터를 찾을 수 없습니다. (최소 3개 열 필요: 주문번호, 주문고유코드, 마켓)");

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

                worksheet.Cell(rowNum, 1).Value = order.OrderCode;
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

    /// <summary>
    /// NPOI 셀값을 문자열로 안전하게 변환
    /// 숫자, 텍스트, 날짜 등 모든 형식 지원
    /// </summary>
    private string GetCellValueAsString(ICell cell)
    {
        if (cell == null)
            return "";

        try
        {
            return cell.CellType switch
            {
                CellType.String => cell.StringCellValue ?? "",
                CellType.Numeric => cell.NumericCellValue.ToString("F0").TrimEnd('0').TrimEnd('.'),
                CellType.Boolean => cell.BooleanCellValue.ToString(),
                CellType.Formula => cell.StringCellValue ?? cell.NumericCellValue.ToString(),
                CellType.Blank => "",
                _ => cell.ToString() ?? ""
            };
        }
        catch
        {
            return cell.ToString() ?? "";
        }
    }
}
