def get_strategies(store, percentile):
    strategies = []

    if percentile.get("배달비율") is not None and percentile["배달비율"] <= 10:
        strategies.append("🚚 배달앱 프로모션 등록으로 신규 유입 확보")

    if percentile.get("재방문율") is not None and percentile["재방문율"] >= 75:
        strategies.append("🎁 생일 쿠폰, 후기 이벤트로 단골 고객 리워드 강화")

    if store.get("주고객층") == "30대 여성":
        strategies.append("📸 감성 메뉴와 포토존, SNS 후기 이벤트 강화")

    if store.get("유입필요고객") == "40대 남성":
        strategies.append("🥡 점심 도시락 구성 및 배달 메뉴 노출 확대")

    if store.get("상권유형") == "직장":
        strategies.append("⏱️ 점심 타임 특화 메뉴와 빠른 회전 강조")

    return strategies
