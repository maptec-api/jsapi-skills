# POI 类目补充

当用户要求按类别检索 POI，或者需要填写 `PlaceSearch.search` 的 `type` / `PlaceSearch.searchNearby` 的 `types` 时，使用本参考。

## 参数规则

- 文本检索：`placeSearch.search(keyword, { type }, callback)`，`type` 为单个类目值。
- 周边检索：`placeSearch.searchNearby({ locationLimit, types }, callback)`，`types` 为逗号分隔类目值。
- 类目值必须使用本文件确认的英文枚举，大小写保持一致。
- 不要使用未确认的通用词作为类型，例如 `school`、`restaurant`、`hotel`、`parking`、`cafe`、`tourist_attraction`。
- 用户输入明确地点名、品牌、校区、地标或地址时，优先只用关键词检索；不确定类目时不要强塞 `type/types`。
- 如果带 `type/types` 返回 `ZERO_RESULTS`，应使用同一关键词去掉类型过滤重试。

## 常用映射

| 用户表达 | 推荐 type/types |
|---|---|
| 大学、学院、university、college | `College_University` |
| 中学 | `Middle_School` |
| 小学 | `Primary_School` |
| 幼儿园 | `Kindergarten` |
| 培训机构 | `Training_Institution` |
| 餐厅、餐馆、restaurant | `Restaurant` |
| 咖啡馆、咖啡、cafe | `Cafe` |
| 酒店、hotel | `Hotels`；细分可用 `Star_Rated_Hotel`、`Budget_Hotel_Chain`、`Luxury_Hotel`、`Resort` |
| 停车场、parking | `Parking`；细分可用 `Indoor_Parking`、`Outdoor_Parking`、`Roadside_Parking` |
| 加油站、gas station | `Gas_Station` |
| 充电站、EV charging | `Ev_Charging_Station` |
| 地铁站、MRT、subway | `Subway_Light_Rail_Station` |
| 火车站 | `Train_Station` |
| 公交站 | `Bus_Stop` |
| 机场 | `Airport` |
| 医院、hospital | `General_Hospital`；细分可用 `Specialized_Hospital`、`Emergency_Center` |
| 诊所、clinic | `Clinics`；细分可用 `Private_Clinic`、`Community_Clinic`、`Dental_Clinic` |
| 药房、pharmacy | `Pharmacy` |
| 银行、bank | `Bank` |
| ATM | `Atm` |
| 商场、购物中心、mall | `Shopping_Mall`；泛化可用 `Shopping_Center` |
| 超市、supermarket | `Supermarket` |
| 便利店 | `Convenience_Store` |
| 公园 | `Urban_Park`；细分可用 `National_Park`、`Nature_Reserve` |
| 博物馆 | `Museum` |
| 图书馆 | `Library` |
| 健身房 | `Gym` |

## 一级类目

- `Transport_Mobility`：交通设施。
- `Entertainment_Leisure`：休闲娱乐。
- `Accommodation`：住宿服务。
- `Corporations_Industry`：公司企业。
- `Health_Medical`：医疗保健。
- `Residential`：房产住宅。
- `Tourism_Culture`：旅游与文化。
- `Government_Organizations`：机构团体。
- `Automotive_Services`：汽车服务。
- `Services_Daily_Life`：生活服务。
- `Geography`：自然地理。
- `Shopping_Retail`：购物零售。
- `Sports_Fitness`：运动健身。
- `Food_Drink`：餐饮美食。

## 交通设施

- 停车服务：`Parking`、`Park_And_Ride`、`Indoor_Parking`、`Roadside_Parking`、`Outdoor_Parking`
- 公路客运：`Bus_Coach`、`Bus_Stop`、`Tourist_Bus_Station`、`Coach_Station`
- 水路出行：`Water_Transport`、`Port_Wharf`、`Marina`、`Ferry_Terminal`
- 空港出行：`Air_Travel`、`Airport`、`Airport_Bus_Stop`、`Helipad`
- 能源补给：`Energy_Facilities`、`Gas_Refill_Station`、`Gas_Station`、`Battery_Swap_Station`、`Ev_Charging_Station`
- 铁路出行：`Rail_Transport`、`Entrance_Exit`、`Ticket_Office`、`Subway_Light_Rail_Station`、`Tram_Stop`、`Train_Station`

## 休闲娱乐与住宿

- 主题乐园：`Theme_Parks`、`Zoo`、`Botanical_Garden`、`Water_Park`、`Aquarium`、`Amusement_Park`
- 休闲场所：`Recreation`、`Ktv`、`Escape_Room_Larp`、`Chess_Card_Room`、`Arcade`、`Internet_Cafe_Esports`
- 影剧院：`Cinema_Theater`、`Theater`、`Opera_House`、`Cinema`、`Concert_Hall`
- 放松疗养：`Wellness`、`Spa`、`Bath_Center_Sauna`、`Beauty_Salon`、`Foot_Massage`
- 住宿服务：`Accommodation`、`Rv_Park`、`Campground`、`Inn`、`Homestay_Short_Term_Rental`、`Motel`、`Hostel`、`Hotels`、`Resort`、`Star_Rated_Hotel`、`Budget_Hotel_Chain`、`Luxury_Hotel`

## 医疗、教育与公共机构

- 医疗保健：`Health_Medical`、`Medical_Examination_Center`、`Veterinary_Clinic`、`Blood_Donation_Station`、`Pharmacy`、`Hospitals`、`Specialized_Hospital`、`Emergency_Center`、`General_Hospital`、`Clinics`、`Psychological_Counseling`、`Dental_Clinic`、`Community_Clinic`、`Private_Clinic`
- 教育机构：`Education`、`Middle_School`、`Training_Institution`、`College_University`、`Primary_School`、`Kindergarten`、`Driving_School`
- 政府机关：`Government`、`Embassy_Consulate`、`City_Hall_Government_Office`、`Courthouse`、`Fire_Station`、`Police_Station`
- 社会团体：`Social_Orgs`、`Association_Society`、`Welfare_House_Nursing_Home`、`Ngo`

## 旅游文化、自然地理与运动

- 公园广场：`Parks_Plazas`、`National_Park`、`Urban_Park`、`Nature_Reserve`、`Street_Plaza`
- 博览场馆：`Museums_Galleries`、`Museum`、`Library`、`Planetarium`、`Archives`、`Science_Museum`、`Art_Gallery`
- 名胜古迹：`Landmarks`、`World_Heritage`、`Historic_Site`、`Historic_Building`、`Monument_Statue`、`Observation_Deck`
- 宗教场所：`Religious_Places`、`Temple`、`Church`、`Mosque`、`Shrine`、`Taoist_Temple`
- 自然地理：`Geography`、`Island`、`River`、`Beach_Coastline`、`Lake`、`Peak`、`Forest`、`Desert`
- 运动健身：`Sports_Fitness`、`Bowling_Alley`、`Climbing_Gym`、`Ski_Resort`、`Tennis_Court`、`Badminton_Court`、`Golf_Course`、`Swimming_Pool`、`Basketball_Court`、`Stadium`、`Soccer_Field`、`Gym`、`Yoga_Pilates_Studio`、`Dance_Studio`

## 购物、生活与公司服务

- 购物中心：`Shopping_Centers`、`Duty_Free_Shop`、`Pedestrian_Street`、`Outlets`、`Department_Store`、`Shopping_Center`、`Shopping_Mall`
- 超市便利：`Groceries`、`Convenience_Store`、`Supermarket`、`Organic_Food_Store`、`Community_Supermarket`、`Market`
- 服饰鞋包：`Fashion_Accessories`、`Clothing_Store`、`Jewelry_Store`、`Luggage_Leather_Goods`、`Sports_Brand_Store`、`Watch_Shop`、`Shoe_Hat_Store`
- 家居建材：`Home_Garden`、`Hardware_Store`、`Furniture_Store`、`Home_Decor`、`Building_Materials_Market`、`Flower_Shop_Garden_Center`
- 生活服务：`Services_Daily_Life`、`Public_Toilet`、`Real_Estate_Agency`、`Laundry`、`Photo_Studio`、`Barber_Shop`、`Repair_Shop`
- 商务服务：`Business`、`Conference_Center`、`Coworking_Space`、`Consulting_Firm`、`Law_Firm`、`Travel_Agency`
- 金融服务：`Financial`、`Atm`、`Insurance_Company`、`Currency_Exchange`、`Bank`
- 公司办公：`Corporations_Industry`、`Offices`、`Corporate_Headquarters`、`Office_Building`、`Industrial_Park`

## 餐饮美食

- 中餐：`Chinese_Cuisine`、`Chinese_Fast_Food`、`Northern_Chinese_Cuisine`、`Sichuan_Cuisine`、`Dim_Sum`、`Halal_Lanzhou_Lamian`、`Hunan_Cuisine`、`Hot_Pot`、`Cantonese_Cuisine`、`General_Chinese_Cuisine`
- 亚洲餐厅：`Asian_Cuisine`、`Southeast_Asian_Cuisine`、`Indian_Cuisine`、`Japanese_Cuisine`、`Thai_Cuisine`、`Vietnamese_Cuisine`、`Korean_Cuisine`
- 咖啡茶饮：`Cafe_Tea_Dessert`、`Ice_Cream_Shop`、`Cafe`、`Milk_Tea_Juice_Shop`、`Dessert_Cake_Shop`、`Teahouse`、`Bakery`
- 快餐小吃：`Fast_Food_Snacks`、`Sandwich_Shop`、`Branded_Fast_Food`、`Salad_Light_Meal`、`Fried_Chicken_Shop`、`Deli`、`Street_Food`
- 西餐：`Western_Cuisine`、`Turkish_Kebab`、`Mexican_Latin_American_Cuisine`、`German_Cuisine`、`Italian_Cuisine`、`French_Cuisine`、`American_Cuisine`、`Spanish_Cuisine`
- 通用餐饮：`Dining_General`、`Restaurant`
- 酒吧夜生活：`Bars_Nightlife`、`Night_Club`、`Izakaya`、`Lounge_Bar`、`Craft_Beer_Bar`、`Bar_Pub`、`Cocktail_Bar`

## Agent 规则

- 用户明确输入类目英文枚举时，按原样使用；只修正明显大小写错误。
- 中文类目要映射到最具体的英文枚举；例如“大学”使用 `College_University`，不是 `school`。
- 用户只说“学校”且无法判断学段时，可以不用 `type`，或询问用户要大学/中学/小学/幼儿园。
- 用户只说“餐饮/吃饭”时，优先用 `Restaurant`；如果用户说咖啡、茶饮、甜品、快餐、火锅等，使用更具体类目。
- 对精准地点名、品牌名、校区名、地标名，不要默认增加类型过滤；类型过滤只用于“按类别找一批地点”的需求。
