import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

# 엑셀 파일 읽기
df = pd.read_excel('U_cities.xlsx', header=1)

# Geocoder 초기화
geolocator = Nominatim(user_agent="myGeocoder")

# 지도 초기 위치 설정 (세종과 대전의 중간 지점으로 설정)
map = folium.Map(location=[36.365, 127.289], zoom_start=17)
print(df.columns)

def geocode_with_retry(address, retries=3):
    for _ in range(retries):
        try:
            location = geolocator.geocode(address)
            if location:
                return location
        except GeocoderTimedOut:
            time.sleep(1)  # 지오코더 타임아웃이 발생하면 잠시 대기
    return None

# 처리된 주소를 추적하기 위한 세트
processed_addresses = set()

# 데이터프레임의 각 행에 대해 반복
for _, row in df.iterrows():
    # 세종과 대전 데이터만 시각화
    if row['City'] in ['세종', '대전광역시']:
        address = row['Address']
        # 주소가 이미 처리되었는지 확인
        if address not in processed_addresses:
            # 주소를 위도와 경도로 변환
            location = geocode_with_retry(address)
            # location이 None이 아닌지 확인
            if location is not None:
                # 변환된 위도와 경도를 사용하여 마커 추가
                folium.Marker(
                    location=[location.latitude, location.longitude],
                    # 팝업 정보에 장소 이름과 주소 추가
                    popup=f"{row['Place']}",#, {row['Address']}",
                ).add_to(map)
                # 처리된 주소로 추가
                processed_addresses.add(address)

# 지도 저장
map.save('map2.html')