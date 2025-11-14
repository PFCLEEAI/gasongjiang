using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace GaSongJang.Models;

/// <summary>
/// 애플리케이션 설정 (마켓별 배송사 선택)
/// AppData에 JSON으로 저장됨
///
/// 구조:
/// {
///   "marketSettings": {
///     "06.쿠팡": "경동택배",
///     "03.11번가": "직접전달",
///     "04.스마트스토어": "경동택배",
///     ...
///   }
/// }
/// </summary>
public class AppSettings
{
    private static readonly string SettingsPath = Path.Combine(
        Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
        "GaSongJang",
        "settings.json"
    );

    /// <summary>
    /// 마켓별 배송사 설정 (마켓이름 → 배송사)
    /// </summary>
    [JsonPropertyName("marketSettings")]
    public Dictionary<string, string> MarketSettings { get; set; } = new();

    /// <summary>
    /// 특정 마켓의 배송사 가져오기
    /// 없으면 기본값 "경동택배" 반환
    /// </summary>
    public string? GetDeliveryCompany(string market)
    {
        if (string.IsNullOrWhiteSpace(market))
            return "경동택배";

        if (MarketSettings.TryGetValue(market, out var company))
        {
            return company;
        }

        return "경동택배";
    }

    /// <summary>
    /// 특정 마켓의 배송사 설정
    /// </summary>
    public void SetDeliveryCompany(string market, string deliveryCompany)
    {
        if (!string.IsNullOrWhiteSpace(market))
        {
            MarketSettings[market] = deliveryCompany;
        }
    }

    /// <summary>
    /// 모든 마켓 목록 가져오기
    /// </summary>
    public IEnumerable<string> GetAllMarkets()
    {
        return MarketSettings.Keys;
    }

    /// <summary>
    /// 설정을 파일에서 로드
    /// 파일이 없으면 기본값 반환
    /// </summary>
    public static AppSettings Load()
    {
        try
        {
            if (File.Exists(SettingsPath))
            {
                string json = File.ReadAllText(SettingsPath);
                var settings = JsonSerializer.Deserialize<AppSettings>(json);
                return settings ?? new AppSettings();
            }
        }
        catch
        {
            // 파일 읽기 실패 시 기본값 반환
        }

        return new AppSettings();
    }

    /// <summary>
    /// 설정을 파일에 저장
    /// </summary>
    public void Save()
    {
        try
        {
            string directory = Path.GetDirectoryName(SettingsPath) ?? "";
            if (!Directory.Exists(directory))
            {
                Directory.CreateDirectory(directory);
            }

            var options = new JsonSerializerOptions
            {
                WriteIndented = true,
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase
            };

            string json = JsonSerializer.Serialize(this, options);
            File.WriteAllText(SettingsPath, json);
        }
        catch (Exception ex)
        {
            throw new Exception($"설정 저장 실패: {ex.Message}", ex);
        }
    }
}
