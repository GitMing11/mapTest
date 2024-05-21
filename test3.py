import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from folium.plugins import MarkerCluster
import time

# 엑셀 파일 읽기
df = pd.read_excel('한국환경공단_전기자동차 충전소 정보현황_20230719.xlsx', header=1)

# Geocoder 초기화
geolocator = Nominatim(user_agent="myGeocoder")

# 지도 초기 위치 설정 (세종과 대전의 중간 지점으로 설정)
map = folium.Map(location=[36.365, 127.289], zoom_start=12)

def geocode_with_retry(address, retries=3):
    for _ in range(retries):
        try:
            location = geolocator.geocode(address)
            if location:
                return location
        except GeocoderTimedOut:
            time.sleep(1)  # 지오코더 타임아웃이 발생하면 잠시 대기
    return None

# MarkerCluster 객체 초기화
marker_cluster = MarkerCluster().add_to(map)

# 데이터프레임의 각 행에 대해 반복
for _, row in df.iterrows():
    # 세종과 대전 데이터만 시각화
    if row['City'] in ['세종특별자치시', '대전광역시']:
        address = row['Address']
        # 주소를 위도와 경도로 변환
        location = geocode_with_retry(address)
        # location이 None이 아닌지 확인
        if location is not None:
            # 변환된 위도와 경도를 사용하여 마커 추가
            folium.Marker(
                location=[location.latitude, location.longitude],
                popup=f"{row['Place']}",
            ).add_to(marker_cluster)  # MarkerCluster에 마커 추가

# 지도 저장
map.save('map_with_marker_cluster2.html')
