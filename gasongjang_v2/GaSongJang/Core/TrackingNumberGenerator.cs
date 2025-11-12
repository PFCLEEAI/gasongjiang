using System.IO;
using System.Text.Json;

namespace GaSongJang.Core;

/// <summary>
/// 송장번호 생성 클래스
/// 형식: YYYYDDDHHMMSSFFF (14자리)
/// - YYYY: 연도 (2025)
/// - DDD: 일년 중 날짜 (001-366)
/// - HH: 시간 (00-23)
/// - MM: 분 (00-59)
/// - SS: 초 (00-59)
/// - FFF: 밀리초/난수 (000-999)
/// </summary>
public class TrackingNumberGenerator
{
    private readonly HashSet<string> _generatedNumbers;
    private readonly string _historyFile;

    public TrackingNumberGenerator()
    {
        _generatedNumbers = new HashSet<string>();
        _historyFile = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
            "GaSongJang",
            "tracking_history.json"
        );

        LoadHistory();
    }

    /// <summary>
    /// 지정된 개수만큼 고유한 송장번호 생성
    /// </summary>
    public List<string> GenerateTrackingNumbers(int count)
    {
        var numbers = new List<string>();
        var random = new Random();

        for (int i = 0; i < count; i++)
        {
            string trackingNumber;
            int attempts = 0;

            // 고유성을 보장하기 위해 최대 100번 시도
            do
            {
                trackingNumber = GenerateUniqueNumber(random);
                attempts++;
            } while (_generatedNumbers.Contains(trackingNumber) && attempts < 100);

            if (attempts < 100)
            {
                numbers.Add(trackingNumber);
                _generatedNumbers.Add(trackingNumber);
            }
        }

        SaveHistory();
        return numbers;
    }

    /// <summary>
    /// 단일 고유 송장번호 생성
    /// </summary>
    private string GenerateUniqueNumber(Random random)
    {
        var now = DateTime.Now;

        // YYYY - 연도 (4자리)
        string yyyy = now.Year.ToString("D4");

        // DDD - 일년 중 날짜 (3자리)
        string ddd = now.DayOfYear.ToString("D3");

        // HH - 시간 (2자리)
        string hh = now.Hour.ToString("D2");

        // MM - 분 (2자리)
        string mm = now.Minute.ToString("D2");

        // SS - 초 (2자리)
        string ss = now.Second.ToString("D2");

        // FFF - 난수 (3자리)
        string fff = random.Next(0, 1000).ToString("D3");

        return $"{yyyy}{ddd}{hh}{mm}{ss}{fff}";
    }

    /// <summary>
    /// 히스토리 파일에서 이전에 생성된 번호들 로드
    /// </summary>
    private void LoadHistory()
    {
        try
        {
            if (File.Exists(_historyFile))
            {
                string json = File.ReadAllText(_historyFile);
                var numbers = System.Text.Json.JsonSerializer.Deserialize<List<string>>(json) ?? new List<string>();
                foreach (var number in numbers)
                {
                    _generatedNumbers.Add(number);
                }
            }
        }
        catch
        {
            // 히스토리 로드 실패 시 무시
        }
    }

    /// <summary>
    /// 생성된 번호들을 히스토리 파일에 저장
    /// </summary>
    private void SaveHistory()
    {
        try
        {
            var dir = Path.GetDirectoryName(_historyFile);
            if (dir != null && !Directory.Exists(dir))
            {
                Directory.CreateDirectory(dir);
            }

            string json = System.Text.Json.JsonSerializer.Serialize(_generatedNumbers.ToList());
            File.WriteAllText(_historyFile, json);
        }
        catch
        {
            // 히스토리 저장 실패 시 무시
        }
    }
}
