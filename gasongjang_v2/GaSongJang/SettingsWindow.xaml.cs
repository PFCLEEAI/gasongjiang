using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using GaSongJang.Models;

namespace GaSongJang;

public partial class SettingsWindow : Window
{
    private AppSettings _settings = null!;
    private Dictionary<string, ComboBox> _marketComboBoxes = new();

    public SettingsWindow(HashSet<string> discoveredMarkets)
    {
        InitializeComponent();
        _settings = AppSettings.Load();
        GenerateMarketUI(discoveredMarkets);
    }

    /// <summary>
    /// 발견된 마켓들에 대해 동적으로 UI 생성
    /// </summary>
    private void GenerateMarketUI(HashSet<string> discoveredMarkets)
    {
        // StackPanel 초기화
        var stackPanel = new StackPanel
        {
            Orientation = Orientation.Vertical,
            Margin = new Thickness(30)
        };

        // 제목
        var title = new Label
        {
            Content = "배송사 설정",
            FontSize = 24,
            FontWeight = System.Windows.FontWeights.Bold,
            Foreground = System.Windows.Media.Brushes.Black,
            Margin = new Thickness(0, 0, 0, 20)
        };
        stackPanel.Children.Add(title);

        // ScrollViewer로 감싸기 (마켓이 많을 수 있음)
        var scrollViewer = new ScrollViewer
        {
            VerticalScrollBarVisibility = ScrollBarVisibility.Auto,
            MaxHeight = 400,
            Margin = new Thickness(0, 0, 0, 20)
        };

        var marketPanel = new StackPanel
        {
            Orientation = Orientation.Vertical
        };

        // 번호 순서대로 정렬
        var sortedMarkets = discoveredMarkets.OrderBy(m =>
        {
            // 숫자로 시작하는 마켓은 번호 순서대로, "Naver"는 맨 뒤
            if (m.StartsWith("0") || m.StartsWith("1"))
            {
                int.TryParse(m.Substring(0, 2), out int num);
                return num * 1000; // 숫자 마켓은 앞에
            }
            return 999999; // "Naver" 등은 맨 뒤
        }).ToList();

        // 각 마켓에 대한 UI 생성
        foreach (var market in sortedMarkets)
        {
            var border = new Border
            {
                Background = new System.Windows.Media.SolidColorBrush(System.Windows.Media.Color.FromRgb(249, 250, 251)),
                CornerRadius = new CornerRadius(8),
                Padding = new Thickness(20),
                Margin = new Thickness(0, 0, 0, 15)
            };

            var marketPanel2 = new StackPanel
            {
                Orientation = Orientation.Vertical
            };

            // 마켓 이름 라벨
            var marketLabel = new Label
            {
                Content = $"📦 {market}",
                FontSize = 14,
                FontWeight = System.Windows.FontWeights.Bold,
                Foreground = System.Windows.Media.Brushes.Black,
                Margin = new Thickness(0, 0, 0, 10)
            };
            marketPanel2.Children.Add(marketLabel);

            // 설명 라벨
            var descLabel = new Label
            {
                Content = "배송사 선택:",
                FontSize = 12,
                Foreground = System.Windows.Media.Brushes.Gray,
                Margin = new Thickness(0, 0, 0, 8)
            };
            marketPanel2.Children.Add(descLabel);

            // ComboBox
            var comboBox = new ComboBox
            {
                FontSize = 12,
                Height = 36,
                Padding = new Thickness(12, 8, 12, 8),
                Background = System.Windows.Media.Brushes.White,
                Foreground = System.Windows.Media.Brushes.Black,
                BorderBrush = new System.Windows.Media.SolidColorBrush(System.Windows.Media.Color.FromRgb(229, 231, 235)),
                BorderThickness = new Thickness(1, 1, 1, 1)
            };

            comboBox.Items.Add("경동택배");
            comboBox.Items.Add("직접전달");
            comboBox.Items.Add("로진택배");
            comboBox.Items.Add("한진택배");
            comboBox.Items.Add("NAVER");

            // 현재 설정값 선택
            string currentCompany = _settings.GetDeliveryCompany(market) ?? "경동택배";
            comboBox.SelectedItem = currentCompany;

            marketPanel2.Children.Add(comboBox);
            border.Child = marketPanel2;

            marketPanel.Children.Add(border);
            _marketComboBoxes[market] = comboBox;
        }

        scrollViewer.Content = marketPanel;
        stackPanel.Children.Add(scrollViewer);

        // 버튼 Grid
        var buttonGrid = new Grid
        {
            Height = 44,
            Margin = new Thickness(0, 20, 0, 0)
        };

        buttonGrid.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
        buttonGrid.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(10) });
        buttonGrid.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });

        var saveButton = new Button
        {
            Content = "💾 저장",
            FontSize = 12,
            FontWeight = System.Windows.FontWeights.Bold,
            Foreground = System.Windows.Media.Brushes.White,
            Background = new System.Windows.Media.SolidColorBrush(System.Windows.Media.Color.FromRgb(31, 41, 55)),
            Cursor = System.Windows.Input.Cursors.Hand,
            Padding = new Thickness(10, 8, 10, 8)
        };
        saveButton.Click += BtnSave_Click;
        Grid.SetColumn(saveButton, 0);
        buttonGrid.Children.Add(saveButton);

        var cancelButton = new Button
        {
            Content = "✕ 취소",
            FontSize = 12,
            FontWeight = System.Windows.FontWeights.Bold,
            Foreground = System.Windows.Media.Brushes.Black,
            Background = new System.Windows.Media.SolidColorBrush(System.Windows.Media.Color.FromRgb(229, 231, 235)),
            Cursor = System.Windows.Input.Cursors.Hand,
            Padding = new Thickness(10, 8, 10, 8)
        };
        cancelButton.Click += BtnCancel_Click;
        Grid.SetColumn(cancelButton, 2);
        buttonGrid.Children.Add(cancelButton);

        stackPanel.Children.Add(buttonGrid);

        // MainGrid에 추가
        var mainGrid = new Grid
        {
            Background = new System.Windows.Media.SolidColorBrush(System.Windows.Media.Color.FromRgb(255, 255, 255))
        };
        mainGrid.Children.Add(stackPanel);

        this.Content = mainGrid;
    }

    /// <summary>
    /// 저장 버튼 클릭
    /// </summary>
    private void BtnSave_Click(object sender, RoutedEventArgs e)
    {
        try
        {
            // 각 마켓의 선택값을 설정에 저장
            foreach (var kvp in _marketComboBoxes)
            {
                string market = kvp.Key;
                ComboBox comboBox = kvp.Value;
                string selectedCompany = comboBox.SelectedItem?.ToString() ?? "경동택배";

                _settings.SetDeliveryCompany(market, selectedCompany);
            }

            // 파일에 저장
            _settings.Save();

            MessageBox.Show("✅ 설정이 저장되었습니다.", "완료", MessageBoxButton.OK, MessageBoxImage.Information);
            this.Close();
        }
        catch (Exception ex)
        {
            MessageBox.Show($"❌ 설정 저장 실패: {ex.Message}", "오류", MessageBoxButton.OK, MessageBoxImage.Error);
        }
    }

    /// <summary>
    /// 취소 버튼 클릭
    /// </summary>
    private void BtnCancel_Click(object sender, RoutedEventArgs e)
    {
        this.Close();
    }
}
