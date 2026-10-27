# 차량 한 대가 사용자의 "필수 조건"을 통과하는지 확인하는 함수들

def is_within_budget(vehicle, preference):
    # MongoDB의 priceFrom은 원 단위
    vehicle_price = vehicle.get("priceFrom")

    # 가격 정보가 없으면 추천 후보에서 제외
    if vehicle_price is None:
        return False

    # 프론트엔드 예산은 만 원 단위이므로 원 단위로 변환
    min_price = preference["minBudget"] * 10000
    max_price = preference["maxBudget"] * 10000

    return min_price <= vehicle_price <= max_price


def matches_body_type(vehicle, preference):
    selected_body_types = preference.get("bodyTypes", [])

    # 차종을 선택하지 않았다면 모든 차종을 허용
    if not selected_body_types:
        return True

    # 여러 차종을 선택했다면 그중 하나와 일치하면 통과
    return vehicle.get("bodyType") in selected_body_types


def matches_powertrain(vehicle, preference):
    selected_powertrains = preference.get("powertrains", [])
    vehicle_powertrain = vehicle.get("powertrain", "")

    # 동력 방식을 선택하지 않았다면 모든 동력 방식을 허용
    if not selected_powertrains:
        return True

    # 예: "가솔린" 선택 시 "가솔린 하이브리드"도 포함할 수 있도록 포함 여부 확인
    return any(
        selected_powertrain in vehicle_powertrain
        for selected_powertrain in selected_powertrains
    )


def matches_origin(vehicle, preference):
    selected_origins = preference.get("origins", [])

    # 국산·수입을 선택하지 않았다면 모두 허용
    if not selected_origins:
        return True

    return vehicle.get("origin") in selected_origins


def matches_features(vehicle, preference):
    selected_features = preference.get("features", [])
    vehicle_features = vehicle.get("features", [])

    # 원하는 기능을 선택하지 않았다면 모두 허용
    if not selected_features:
        return True

    # 기능을 여러 개 선택했다면 모두 있어야 통과
    return all(
        selected_feature in vehicle_features
        for selected_feature in selected_features
    )


def matches_required_conditions(vehicle, preference):
    # 선택한 조건은 점수가 아니라 "통과 또는 탈락" 기준으로 사용
    return (
        is_within_budget(vehicle, preference)
        and matches_body_type(vehicle, preference)
        and matches_powertrain(vehicle, preference)
        and matches_origin(vehicle, preference)
        and matches_features(vehicle, preference)
    )


def score_vehicle(vehicle, preference):
    # 이 함수에 들어온 차량은 이미 필수 조건을 모두 통과한 상태
    reasons = ["예산 범위 일치"]

    if preference.get("bodyTypes"):
        reasons.append("선호 차종 일치")

    if preference.get("powertrains"):
        reasons.append("동력 방식 일치")

    if preference.get("origins"):
        reasons.append("국산·수입 선택 일치")

    if preference.get("features"):
        reasons.append("필수 기능 일치")

    # 원본 데이터를 직접 변경하지 않도록 복사
    result = vehicle.copy()

    # 일치한 조건 수를 점수로 사용
    result["score"] = len(reasons)
    result["reasons"] = reasons

    return result


def rank_vehicles(vehicles, preference):
    # 1. 사용자가 선택한 필수 조건을 모두 통과한 차량만 남김
    matched_vehicles = [
        vehicle
        for vehicle in vehicles
        if matches_required_conditions(vehicle, preference)
    ]

    # 2. 추천 근거와 점수를 추가
    scored_vehicles = [
        score_vehicle(vehicle, preference)
        for vehicle in matched_vehicles
    ]

    # 3. 조건 일치 점수가 같으면 시작 가격이 낮은 차량을 먼저 보여줌
    return sorted(
        scored_vehicles,
        key=lambda vehicle: (
            -vehicle["score"],
            vehicle.get("priceFrom", float("inf")),
        ),
    )