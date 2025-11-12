namespace GaSongJang.Models;

/// <summary>
/// 주문 데이터 모델
/// </summary>
public class OrderData
{
    /// <summary>
    /// 주문 고유 코드
    /// </summary>
    public string OrderID { get; set; } = string.Empty;

    /// <summary>
    /// 마켓 이름 (판매처)
    /// </summary>
    public string MarketName { get; set; } = string.Empty;

    /// <summary>
    /// 생성된 송장번호
    /// </summary>
    public string TrackingNumber { get; set; } = string.Empty;

    /// <summary>
    /// 택배사 (배송 회사)
    /// </summary>
    public string DeliveryCompany { get; set; } = string.Empty;

    /// <summary>
    /// 조건에 따라 배송 회사 설정 및 송장번호 처리
    /// - MarketName에 "11번가" 또는 "스마트스토어"가 포함되면 "직접전달" (송장번호 제거)
    /// - 그 외에는 "경동택배" (송장번호 필요)
    /// </summary>
    public void SetDeliveryCompany()
    {
        if (string.IsNullOrWhiteSpace(MarketName))
        {
            DeliveryCompany = "경동택배";
            return;
        }

        if (MarketName.Contains("11번가") || MarketName.Contains("스마트스토어"))
        {
            DeliveryCompany = "직접전달";
            TrackingNumber = string.Empty;  // 직접전달은 송장번호 불필요
        }
        else
        {
            DeliveryCompany = "경동택배";
            // TrackingNumber는 나중에 생성 로직에서 설정
        }
    }
}
