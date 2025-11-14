namespace GaSongJang.Models;

/// <summary>
/// 주문 데이터 모델
/// </summary>
public class OrderData
{
    /// <summary>
    /// 주문 번호
    /// </summary>
    public string OrderID { get; set; } = string.Empty;

    /// <summary>
    /// 주문 고유 코드
    /// </summary>
    public string OrderCode { get; set; } = string.Empty;

    /// <summary>
    /// 마켓 (판매처 플랫폼)
    /// 예: "06.쿠팡", "03.11번가", "04.스마트스토어" 등
    /// </summary>
    public string Market { get; set; } = string.Empty;

    /// <summary>
    /// 생성된 송장번호
    /// </summary>
    public string TrackingNumber { get; set; } = string.Empty;

    /// <summary>
    /// 택배사 (배송 회사)
    /// </summary>
    public string DeliveryCompany { get; set; } = string.Empty;

    /// <summary>
    /// Market 설정에 따라 배송 회사 자동 할당
    /// AppSettings에서 마켓별 배송사를 읽어 적용
    /// 기본값: "경동택배"
    /// </summary>
    public void SetDeliveryCompany()
    {
        var settings = AppSettings.Load();

        if (string.IsNullOrWhiteSpace(Market))
        {
            DeliveryCompany = "경동택배";
            return;
        }

        // Market에서 설정된 배송사 가져오기
        // Market이 설정에 없으면 기본값 "경동택배" 사용
        DeliveryCompany = settings.GetDeliveryCompany(Market) ?? "경동택배";

        // 직접전달이면 송장번호는 불필요
        if (DeliveryCompany == "직접전달")
        {
            TrackingNumber = string.Empty;
        }
    }
}
