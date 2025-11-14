using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Windows;
using Microsoft.Win32;
using GaSongJang.Core;
using GaSongJang.Models;

namespace GaSongJang;

public partial class MainWindow : Window
{
    private TrackingNumberGenerator trackingGenerator = null!;
    private ExcelProcessor excelProcessor = null!;
    private ObservableCollection<OrderData> orders = new();
    private List<string> trackingNumbers = new();
    private HashSet<string> discoveredMarkets = new();

    public MainWindow()
    {
        InitializeComponent();
        trackingGenerator = new TrackingNumberGenerator();
        excelProcessor = new ExcelProcessor();
        DgvMarkets.ItemsSource = orders;

        // Populate delivery company dropdown options
        var deliveryCompanies = new List<string>
        {
            "직접전달",
            "경동택배",
            "로진택배",
            "한진택배",
            "NAVER"
        };

        var deliveryCompanyColumn = DgvMarkets.Columns
            .OfType<System.Windows.Controls.DataGridComboBoxColumn>()
            .FirstOrDefault();

        if (deliveryCompanyColumn != null)
        {
            deliveryCompanyColumn.ItemsSource = deliveryCompanies;
        }
    }

    private void BtnUpload_Click(object sender, RoutedEventArgs e)
    {
        try
        {
            var openFileDialog = new OpenFileDialog
            {
                Title = "Excel 파일 선택",
                Filter = "Excel Files|*.xls;*.xlsx|All Files|*.*"
            };

            if (openFileDialog.ShowDialog() != true)
                return;

            StatusLabel.Text = "📂 파일 로딩 중...";
            StatusLabel.Foreground = Application.Current.Resources["TextGrayBrush"] as System.Windows.Media.Brush;

            var loadedOrders = excelProcessor.ReadExcelFile(openFileDialog.FileName);

            orders.Clear();
            discoveredMarkets.Clear();

            foreach (var order in loadedOrders)
            {
                order.SetDeliveryCompany();
                orders.Add(order);
                discoveredMarkets.Add(order.Market);
            }

            StatusLabel.Text = $"✅ 파일 로드 완료 ({orders.Count}개 항목)";
            StatusLabel.Foreground = Application.Current.Resources["SuccessGreenBrush"] as System.Windows.Media.Brush;
            trackingNumbers.Clear();

            BtnGenerate.IsEnabled = true;
            BtnDownload.IsEnabled = false;
        }
        catch (Exception ex)
        {
            MessageBox.Show($"파일 로드 실패:\n\n{ex.Message}", "오류",
                MessageBoxButton.OK, MessageBoxImage.Error);
            ResetUI();
        }
    }

    private void BtnGenerate_Click(object sender, RoutedEventArgs e)
    {
        try
        {
            if (orders.Count == 0)
            {
                MessageBox.Show("먼저 Excel 파일을 선택하세요.", "알림",
                    MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }

            BtnUpload.IsEnabled = false;
            BtnGenerate.IsEnabled = false;
            BtnDownload.IsEnabled = false;

            StatusLabel.Text = "🔄 송장번호 생성 중...";
            StatusLabel.Foreground = Application.Current.Resources["TextGrayBrush"] as System.Windows.Media.Brush;

            // Step 1: Update orders with selected delivery companies from DataGrid
            for (int i = 0; i < orders.Count; i++)
            {
                var order = orders[i];
                // DeliveryCompany is already bound to ComboBox, so it's already updated
            }

            // Step 2: Count how many orders need tracking numbers (only "경동택배")
            int trackingNumberNeededCount = orders.Count(o => o.DeliveryCompany == "경동택배");

            // Step 3: Generate tracking numbers only for "경동택배"
            if (trackingNumberNeededCount > 0)
            {
                trackingNumbers = trackingGenerator.GenerateTrackingNumbers(trackingNumberNeededCount);
            }

            // Step 4: Assign tracking numbers based on delivery company
            int trackingNumberIndex = 0;
            for (int i = 0; i < orders.Count; i++)
            {
                if (orders[i].DeliveryCompany == "경동택배")
                {
                    orders[i].TrackingNumber = trackingNumbers[trackingNumberIndex];
                    trackingNumberIndex++;
                }
                else
                {
                    orders[i].TrackingNumber = string.Empty;
                }
            }

            // Refresh DataGrid
            DgvMarkets.Items.Refresh();

            // Show completion
            StatusLabel.Text = "✅ 송장번호 생성 완료";
            StatusLabel.Foreground = Application.Current.Resources["SuccessGreenBrush"] as System.Windows.Media.Brush;

            System.Threading.Thread.Sleep(500);

            // Show completion message
            MessageBox.Show("✅ 송장번호 생성이 완료되었습니다!\n\nExcel 다운로드 버튼을 클릭하여 결과를 저장하세요.", "완료",
                MessageBoxButton.OK, MessageBoxImage.Information);

            BtnUpload.IsEnabled = true;
            BtnDownload.IsEnabled = true;
        }
        catch (Exception ex)
        {
            MessageBox.Show($"생성 실패:\n\n{ex.Message}", "오류",
                MessageBoxButton.OK, MessageBoxImage.Error);
            BtnUpload.IsEnabled = true;
            BtnGenerate.IsEnabled = orders.Count > 0;
            BtnDownload.IsEnabled = false;
        }
    }

    private void BtnDownload_Click(object sender, RoutedEventArgs e)
    {
        try
        {
            if (orders.Count == 0 || (trackingNumbers.Count == 0 && orders.Any(o => o.DeliveryCompany == "경동택배")))
            {
                MessageBox.Show("먼저 송장번호를 생성하세요.", "알림",
                    MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }

            var saveFileDialog = new SaveFileDialog
            {
                Title = "파일 저장",
                Filter = "Excel Files (*.xlsx)|*.xlsx",
                FileName = $"가송장_생성기_{DateTime.Now:yyyyMMdd_HHmmss}.xlsx"
            };

            if (saveFileDialog.ShowDialog() != true)
                return;

            StatusLabel.Text = "💾 파일 저장 중...";
            StatusLabel.Foreground = Application.Current.Resources["TextGrayBrush"] as System.Windows.Media.Brush;

            var orderList = new List<OrderData>(orders);
            excelProcessor.WriteExcelFile(orderList, saveFileDialog.FileName);

            StatusLabel.Text = "✅ 파일 저장 완료";
            StatusLabel.Foreground = Application.Current.Resources["SuccessGreenBrush"] as System.Windows.Media.Brush;

            MessageBox.Show($"저장 완료!\n\n{saveFileDialog.FileName}", "완료",
                MessageBoxButton.OK, MessageBoxImage.Information);

            ResetForNewOperation();
        }
        catch (Exception ex)
        {
            MessageBox.Show($"저장 실패:\n\n{ex.Message}", "오류",
                MessageBoxButton.OK, MessageBoxImage.Error);
        }
    }

    private void ResetUI()
    {
        StatusLabel.Text = "📂 파일을 선택하세요";
        StatusLabel.Foreground = Application.Current.Resources["TextGrayBrush"] as System.Windows.Media.Brush;
        orders.Clear();

        BtnUpload.IsEnabled = true;
        BtnGenerate.IsEnabled = false;
        BtnDownload.IsEnabled = false;
    }

    private void ResetForNewOperation()
    {
        orders.Clear();
        trackingNumbers.Clear();
        ResetUI();
    }

    /// <summary>
    /// 설정 메뉴 클릭 이벤트
    /// </summary>
    private void MenuSettings_Click(object sender, RoutedEventArgs e)
    {
        // 발견된 마켓이 없으면, 저장된 설정에서 마켓 로드
        HashSet<string> marketsToShow = discoveredMarkets.Count > 0
            ? discoveredMarkets
            : new HashSet<string>(AppSettings.Load().GetAllMarkets());

        // 마켓이 전혀 없으면 기본 마켓 제시
        if (marketsToShow.Count == 0)
        {
            marketsToShow = new HashSet<string>
            {
                "02.옥션",
                "03.11번가",
                "04.스마트스토어",
                "06.쿠팡",
                "Naver"
            };
        }

        // 번호 순서대로 정렬
        var sortedMarkets = marketsToShow.OrderBy(m =>
        {
            // 숫자로 시작하는 마켓은 번호 순서대로, "Naver"는 맨 뒤
            if (m.StartsWith("0") || m.StartsWith("1"))
            {
                int.TryParse(m.Substring(0, 2), out int num);
                return num * 1000; // 숫자 마켓은 앞에
            }
            return 999999; // "Naver" 등은 맨 뒤
        }).ToList();

        var settingsWindow = new SettingsWindow(new HashSet<string>(sortedMarkets))
        {
            Owner = this
        };
        settingsWindow.ShowDialog();

        // 설정이 변경되었으므로 현재 주문들의 배송사 다시 계산
        foreach (var order in orders)
        {
            order.SetDeliveryCompany();
        }
        DgvMarkets.Items.Refresh();
    }
}
