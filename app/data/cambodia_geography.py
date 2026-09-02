"""Cambodia 25 Provinces & Major Districts Geography Dataset.

Provides bilingual (English & Khmer) names, centroid coordinates for
spatial mapping, district cascades, nearest-province Haversine lookup,
and legacy location string normalizers.
"""

import math

CAMBODIA_PROVINCES = [
    {
        "code": "phnom_penh",
        "name_en": "Phnom Penh",
        "name_km": "ភ្នំពេញ",
        "lat": 11.5564,
        "lng": 104.9282,
        "districts": [
            {"name_en": "Chamkar Mon", "name_km": "ចំការមន"},
            {"name_en": "Doun Penh", "name_km": "ដូនពេញ"},
            {"name_en": "Prampir Meakkakra", "name_km": "៧មករា"},
            {"name_en": "Tuol Kouk", "name_km": "ទួលគោក"},
            {"name_en": "Dangkao", "name_km": "ដង្កោ"},
            {"name_en": "Mean Chey", "name_km": "មានជ័យ"},
            {"name_en": "Russey Keo", "name_km": "ឫស្សីកែវ"},
            {"name_en": "Sen Sok", "name_km": "សែនសុខ"},
            {"name_en": "Pou Senchey", "name_km": "ពោធិ៍សែនជ័យ"},
            {"name_en": "Chroy Changvar", "name_km": "ជ្រោយចង្វារ"},
            {"name_en": "Prek Pnov", "name_km": "ព្រែកព្នៅ"},
            {"name_en": "Chbar Ampov", "name_km": "ច្បារអំពៅ"},
            {"name_en": "Boeng Keng Kang", "name_km": "បឹងកេងកង"},
            {"name_en": "Kamboul", "name_km": "កំបូល"},
        ],
    },
    {
        "code": "kandal",
        "name_en": "Kandal",
        "name_km": "កណ្តាល",
        "lat": 11.4556,
        "lng": 104.9665,
        "districts": [
            {"name_en": "Krong Ta Khmau", "name_km": "ក្រុងតាខ្មៅ"},
            {"name_en": "Kandal Stueng", "name_km": "កណ្តាលស្ទឹង"},
            {"name_en": "Kien Svay", "name_km": "កៀនស្វាយ"},
            {"name_en": "Khsach Kandal", "name_km": "ខ្សាច់កណ្តាល"},
            {"name_en": "Koh Thom", "name_km": "កោះធំ"},
            {"name_en": "Leuk Daek", "name_km": "លើកដែក"},
            {"name_en": "Lvea Aem", "name_km": "ល្វាឯម"},
            {"name_en": "Mukh Kampul", "name_km": "មុខកំពូល"},
            {"name_en": "Angk Snuol", "name_km": "អង្គស្នួល"},
            {"name_en": "Ponhea Lueu", "name_km": "ពញាឮ"},
            {"name_en": "S'ang", "name_km": "ស្អាង"},
        ],
    },
    {
        "code": "kampong_cham",
        "name_en": "Kampong Cham",
        "name_km": "កំពង់ចាម",
        "lat": 12.0000,
        "lng": 105.4500,
        "districts": [
            {"name_en": "Krong Kampong Cham", "name_km": "ក្រុងកំពង់ចាម"},
            {"name_en": "Batheay", "name_km": "បាធាយ"},
            {"name_en": "Chamkar Leu", "name_km": "ចំការលើ"},
            {"name_en": "Cheung Prey", "name_km": "ជើងព្រៃ"},
            {"name_en": "Kampong Siem", "name_km": "កំពង់សៀម"},
            {"name_en": "Kang Meas", "name_km": "កងមាស"},
            {"name_en": "Koh Sotin", "name_km": "កោះសូទិន"},
            {"name_en": "Prey Chhor", "name_km": "ព្រៃឈរ"},
            {"name_en": "Srey Santhor", "name_km": "ស្រីសន្ធរ"},
            {"name_en": "Stueng Trang", "name_km": "ស្ទឹងត្រង់"},
        ],
    },
    {
        "code": "kampong_chhnang",
        "name_en": "Kampong Chhnang",
        "name_km": "កំពង់ឆ្នាំង",
        "lat": 12.2500,
        "lng": 104.6667,
        "districts": [
            {"name_en": "Krong Kampong Chhnang", "name_km": "ក្រុងកំពង់ឆ្នាំង"},
            {"name_en": "Baribour", "name_km": "បរិបូណ៌"},
            {"name_en": "Chol Kiri", "name_km": "ជលគិរី"},
            {"name_en": "Kampong Leaeng", "name_km": "កំពង់លែង"},
            {"name_en": "Kampong Tralach", "name_km": "កំពង់ត្រឡាច"},
            {"name_en": "Rolea B'ier", "name_km": "រលាប្អៀរ"},
            {"name_en": "Sameakki Mean Chey", "name_km": "សាមគ្គីមានជ័យ"},
            {"name_en": "Tuek Phos", "name_km": "ទឹកផុស"},
        ],
    },
    {
        "code": "kampong_speu",
        "name_en": "Kampong Speu",
        "name_km": "កំពង់ស្ពឺ",
        "lat": 11.4500,
        "lng": 104.5167,
        "districts": [
            {"name_en": "Krong Chbar Mon", "name_km": "ក្រុងច្បារមន"},
            {"name_en": "Basedth", "name_km": "បាសិត"},
            {"name_en": "Kong Pisei", "name_km": "គងពិសី"},
            {"name_en": "Aoral", "name_km": "ឱរ៉ាល់"},
            {"name_en": "Odongk", "name_km": "ឧដុង្គ"},
            {"name_en": "Phnom Sruoch", "name_km": "ភ្នំស្រួច"},
            {"name_en": "Samraong Tong", "name_km": "សំរោងទង"},
            {"name_en": "Thpong", "name_km": "ថ្ពង"},
        ],
    },
    {
        "code": "kampong_thom",
        "name_en": "Kampong Thom",
        "name_km": "កំពង់ធំ",
        "lat": 12.7111,
        "lng": 104.8889,
        "districts": [
            {"name_en": "Krong Stueng Saen", "name_km": "ក្រុងស្ទឹងសែន"},
            {"name_en": "Baray", "name_km": "បារាយណ៍"},
            {"name_en": "Kampong Svay", "name_km": "កំពង់ស្វាយ"},
            {"name_en": "Prasat Balangk", "name_km": "ប្រាសាទបល្ល័ង្ក"},
            {"name_en": "Prasat Sambour", "name_km": "ប្រាសាទសំបូរ"},
            {"name_en": "Sandan", "name_km": "សណ្តាន់"},
            {"name_en": "Santuk", "name_km": "សន្ទុក"},
            {"name_en": "Stoung", "name_km": "ស្ទោង"},
            {"name_en": "Taing Kouk", "name_km": "តាំងគោក"},
        ],
    },
    {
        "code": "siem_reap",
        "name_en": "Siem Reap",
        "name_km": "សៀមរាប",
        "lat": 13.3618,
        "lng": 103.8606,
        "districts": [
            {"name_en": "Krong Siem Reap", "name_km": "ក្រុងសៀមរាប"},
            {"name_en": "Angkor Chum", "name_km": "អង្គរជុំ"},
            {"name_en": "Angkor Thum", "name_km": "អង្គរធំ"},
            {"name_en": "Banteay Srei", "name_km": "បន្ទាយស្រី"},
            {"name_en": "Chi Kraeng", "name_km": "ជីក្រែង"},
            {"name_en": "Kralanh", "name_km": "ក្រឡាញ់"},
            {"name_en": "Puok", "name_km": "ពួក"},
            {"name_en": "Prasat Bakong", "name_km": "ប្រាសាទបាគង"},
            {"name_en": "Soutr Nikom", "name_km": "សូទ្រនិគម"},
            {"name_en": "Srei Snam", "name_km": "ស្រីស្នំ"},
            {"name_en": "Svay Leu", "name_km": "ស្វាយលើ"},
            {"name_en": "Varin", "name_km": "វ៉ារិន"},
        ],
    },
    {
        "code": "battambang",
        "name_en": "Battambang",
        "name_km": "បាត់ដំបង",
        "lat": 13.1027,
        "lng": 103.1982,
        "districts": [
            {"name_en": "Krong Battambang", "name_km": "ក្រុងបាត់ដំបង"},
            {"name_en": "Banan", "name_km": "បាណន់"},
            {"name_en": "Thma Koul", "name_km": "ថ្មគោល"},
            {"name_en": "Bavel", "name_km": "បវេល"},
            {"name_en": "Ek Phnom", "name_km": "ឯកភ្នំ"},
            {"name_en": "Moung Ruessei", "name_km": "មោងឫស្សី"},
            {"name_en": "Rottanak Mondol", "name_km": "រតនមណ្ឌល"},
            {"name_en": "Sangkae", "name_km": "សង្កែ"},
            {"name_en": "Samlout", "name_km": "សំឡូត"},
            {"name_en": "Sampov Loun", "name_km": "សំពៅលូន"},
            {"name_en": "Phnum Proek", "name_km": "ភ្នំព្រឹក"},
            {"name_en": "Kamrieng", "name_km": "កំរៀង"},
            {"name_en": "Koas Krala", "name_km": "គាស់ក្រឡ"},
            {"name_en": "Rukh Kiri", "name_km": "រុក្ខគិរី"},
        ],
    },
    {
        "code": "banteay_meanchey",
        "name_en": "Banteay Meanchey",
        "name_km": "បន្ទាយមានជ័យ",
        "lat": 13.5859,
        "lng": 102.9737,
        "districts": [
            {"name_en": "Krong Serei Saophoan", "name_km": "ក្រុងសិរីសោភ័ណ"},
            {"name_en": "Krong Poipet", "name_km": "ក្រុងប៉ោយប៉ែត"},
            {"name_en": "Mongkol Borei", "name_km": "មង្គលបូរី"},
            {"name_en": "Phnom Srok", "name_km": "ភ្នំស្រុក"},
            {"name_en": "Preah Netr Preah", "name_km": "ព្រះនេត្រព្រះ"},
            {"name_en": "Ou Chrov", "name_km": "អូរជ្រៅ"},
            {"name_en": "Thma Puok", "name_km": "ថ្មពួក"},
            {"name_en": "Svay Chek", "name_km": "ស្វាយចេក"},
            {"name_en": "Malai", "name_km": "ម៉ាឡៃ"},
        ],
    },
    {
        "code": "prey_veng",
        "name_en": "Prey Veng",
        "name_km": "ព្រៃវែង",
        "lat": 11.4868,
        "lng": 105.3253,
        "districts": [
            {"name_en": "Krong Prey Veng", "name_km": "ក្រុងព្រៃវែង"},
            {"name_en": "Ba Phnum", "name_km": "បាភ្នំ"},
            {"name_en": "Kamchay Mear", "name_km": "កំចាយមារ"},
            {"name_en": "Kampong Trabaek", "name_km": "កំពង់ត្របែក"},
            {"name_en": "Kanhchriech", "name_km": "កញ្ច្រៀច"},
            {"name_en": "Me Sang", "name_km": "មេសាង"},
            {"name_en": "Peam Chor", "name_km": "ពាមជរ"},
            {"name_en": "Peam Ro", "name_km": "ពាមរក៍"},
            {"name_en": "Pea Reang", "name_km": "ពារាំង"},
            {"name_en": "Preah Sdach", "name_km": "ព្រះស្តេច"},
            {"name_en": "Svay Antor", "name_km": "ស្វាយអន្ធរ"},
            {"name_en": "Sithor Kandal", "name_km": "ស៊ីធរកណ្តាល"},
        ],
    },
    {
        "code": "svay_rieng",
        "name_en": "Svay Rieng",
        "name_km": "ស្វាយរៀង",
        "lat": 11.0879,
        "lng": 105.7994,
        "districts": [
            {"name_en": "Krong Svay Rieng", "name_km": "ក្រុងស្វាយរៀង"},
            {"name_en": "Krong Bavet", "name_km": "ក្រុងបាវិត"},
            {"name_en": "Chantrea", "name_km": "ចន្ទ្រា"},
            {"name_en": "Kampong Rou", "name_km": "កំពង់រោទិ៍"},
            {"name_en": "Romeas Haek", "name_km": "រមាសហែក"},
            {"name_en": "Svay Chrum", "name_km": "ស្វាយជ្រំ"},
            {"name_en": "Svay Teap", "name_km": "ស្វាយទាប"},
            {"name_en": "Romdoul", "name_km": "រំដួល"},
        ],
    },
    {
        "code": "takeo",
        "name_en": "Takeo",
        "name_km": "តាកែវ",
        "lat": 10.9908,
        "lng": 104.7850,
        "districts": [
            {"name_en": "Krong Doun Kaev", "name_km": "ក្រុងដូនកែវ"},
            {"name_en": "Angkor Borei", "name_km": "អង្គរបូរី"},
            {"name_en": "Bati", "name_km": "បាទី"},
            {"name_en": "Borei Cholsar", "name_km": "បូរីជលសារ"},
            {"name_en": "Kiri Vong", "name_km": "គិរីវង់"},
            {"name_en": "Koh Andaet", "name_km": "កោះអណ្តែត"},
            {"name_en": "Prey Kabbas", "name_km": "ព្រៃកប្បាស"},
            {"name_en": "Samraong", "name_km": "សំរោង"},
            {"name_en": "Tram Kak", "name_km": "ត្រាំកក់"},
            {"name_en": "Treang", "name_km": "ទ្រាំង"},
        ],
    },
    {
        "code": "kampot",
        "name_en": "Kampot",
        "name_km": "កំពត",
        "lat": 10.6104,
        "lng": 104.1815,
        "districts": [
            {"name_en": "Krong Kampot", "name_km": "ក្រុងកំពត"},
            {"name_en": "Angkor Chey", "name_km": "អង្គរជ័យ"},
            {"name_en": "Banteay Meas", "name_km": "បន្ទាយមាស"},
            {"name_en": "Chhouk", "name_km": "ឈូក"},
            {"name_en": "Chum Kiri", "name_km": "ជុំគិរី"},
            {"name_en": "Dang Tong", "name_km": "ដងទង់"},
            {"name_en": "Kampong Trach", "name_km": "កំពង់ត្រាច"},
            {"name_en": "Tuek Chhou", "name_km": "ទឹកឈូ"},
        ],
    },
    {
        "code": "kep",
        "name_en": "Kep",
        "name_km": "កែប",
        "lat": 10.4829,
        "lng": 104.2949,
        "districts": [
            {"name_en": "Krong Kep", "name_km": "ក្រុងកែប"},
            {"name_en": "Damnak Chang'aeur", "name_km": "ដំណាក់ចង្អើរ"},
        ],
    },
    {
        "code": "preah_sihanouk",
        "name_en": "Preah Sihanouk",
        "name_km": "ព្រះសីហនុ",
        "lat": 10.6275,
        "lng": 103.5221,
        "districts": [
            {"name_en": "Krong Preah Sihanouk", "name_km": "ក្រុងព្រះសីហនុ"},
            {"name_en": "Prey Nob", "name_km": "ព្រៃនប់"},
            {"name_en": "Stueng Hav", "name_km": "ស្ទឹងហាវ"},
            {"name_en": "Kampong Seila", "name_km": "កំពង់សិលា"},
            {"name_en": "Krong Koh Rong", "name_km": "ក្រុងកោះរ៉ុង"},
        ],
    },
    {
        "code": "koh_kong",
        "name_en": "Koh Kong",
        "name_km": "កោះកុង",
        "lat": 11.6153,
        "lng": 102.9838,
        "districts": [
            {"name_en": "Krong Khemarak Phoumin", "name_km": "ក្រុងខេមរភូមិន្ទ"},
            {"name_en": "Botum Sakor", "name_km": "បទុមសាគរ"},
            {"name_en": "Kiri Sakor", "name_km": "គិរីសាគរ"},
            {"name_en": "Koh Kong", "name_km": "កោះកុង"},
            {"name_en": "Mondol Seima", "name_km": "មណ្ឌលសីមា"},
            {"name_en": "Srae Ambel", "name_km": "ស្រែអំបិល"},
            {"name_en": "Thma Bang", "name_km": "ថ្មបាំង"},
        ],
    },
    {
        "code": "pursat",
        "name_en": "Pursat",
        "name_km": "ពោធិ៍សាត់",
        "lat": 12.5388,
        "lng": 103.9192,
        "districts": [
            {"name_en": "Krong Pursat", "name_km": "ក្រុងពោធិ៍សាត់"},
            {"name_en": "Bakan", "name_km": "បាកាន"},
            {"name_en": "Kandieng", "name_km": "កណ្តៀង"},
            {"name_en": "Krakor", "name_km": "ក្រគរ"},
            {"name_en": "Phnum Kravanh", "name_km": "ភ្នំក្រវាញ"},
            {"name_en": "Veal Veaeng", "name_km": "វាលវែង"},
            {"name_en": "Talou Sen Chey", "name_km": "តាលោសែនជ័យ"},
        ],
    },
    {
        "code": "pailin",
        "name_en": "Pailin",
        "name_km": "ប៉ៃលិន",
        "lat": 12.8489,
        "lng": 102.6093,
        "districts": [
            {"name_en": "Krong Pailin", "name_km": "ក្រុងប៉ៃលិន"},
            {"name_en": "Sala Krau", "name_km": "សាលាក្រៅ"},
        ],
    },
    {
        "code": "oddar_meanchey",
        "name_en": "Oddar Meanchey",
        "name_km": "ឧត្តរមានជ័យ",
        "lat": 14.1673,
        "lng": 103.5168,
        "districts": [
            {"name_en": "Krong Samraong", "name_km": "ក្រុងសំរោង"},
            {"name_en": "Anlong Veaeng", "name_km": "អន្លង់វែង"},
            {"name_en": "Banteay Ampil", "name_km": "បន្ទាយអំពិល"},
            {"name_en": "Chong Kal", "name_km": "ចុងកាល់"},
            {"name_en": "Trapeang Prasat", "name_km": "ត្រពាំងប្រាសាទ"},
        ],
    },
    {
        "code": "preah_vihear",
        "name_en": "Preah Vihear",
        "name_km": "ព្រះវិហារ",
        "lat": 13.8073,
        "lng": 104.9811,
        "districts": [
            {"name_en": "Krong Preah Vihear", "name_km": "ក្រុងព្រះវិហារ"},
            {"name_en": "Chey Saen", "name_km": "ជ័យសែន"},
            {"name_en": "Chhaeb", "name_km": "ឆែប"},
            {"name_en": "Choam Khsant", "name_km": "ជាំក្សាន្ត"},
            {"name_en": "Kuleaen", "name_km": "គូលែន"},
            {"name_en": "Rovieng", "name_km": "រវៀង"},
            {"name_en": "Sangkum Thmei", "name_km": "សង្គមថ្មី"},
            {"name_en": "Tbaeng Mean Chey", "name_km": "ត្បែងមានជ័យ"},
        ],
    },
    {
        "code": "stung_treng",
        "name_en": "Stung Treng",
        "name_km": "ស្ទឹងត្រែង",
        "lat": 13.5259,
        "lng": 105.9683,
        "districts": [
            {"name_en": "Krong Stung Treng", "name_km": "ក្រុងស្ទឹងត្រែង"},
            {"name_en": "Sesan", "name_km": "សេសាន"},
            {"name_en": "Siem Bouk", "name_km": "សៀមបូក"},
            {"name_en": "Siem Pang", "name_km": "សៀមប៉ាង"},
            {"name_en": "Thala Barivat", "name_km": "ថាឡាបារីវ៉ាត់"},
            {"name_en": "Borei O’Svay Sen Chey", "name_km": "បុរីអូរស្វាយសែនជ័យ"},
        ],
    },
    {
        "code": "kratie",
        "name_en": "Kratie",
        "name_km": "ក្រចេះ",
        "lat": 12.4881,
        "lng": 106.0188,
        "districts": [
            {"name_en": "Krong Kratie", "name_km": "ក្រុងក្រចេះ"},
            {"name_en": "Chhloung", "name_km": "ឆ្លូង"},
            {"name_en": "Prek Prasab", "name_km": "ព្រែកប្រសព្វ"},
            {"name_en": "Sambour", "name_km": "សំបូរ"},
            {"name_en": "Snuol", "name_km": "ស្នួល"},
            {"name_en": "Chet Borei", "name_km": "ចិត្របុរី"},
        ],
    },
    {
        "code": "mondulkiri",
        "name_en": "Mondulkiri",
        "name_km": "មណ្ឌលគិរី",
        "lat": 12.4558,
        "lng": 107.1881,
        "districts": [
            {"name_en": "Krong Saen Monourom", "name_km": "ក្រុងសែនមនោរម្យ"},
            {"name_en": "Kaoh Nheaek", "name_km": "កោះញែក"},
            {"name_en": "Ou Reang", "name_km": "អូររាំង"},
            {"name_en": "Pech Chreada", "name_km": "ពេជ្រាដា"},
            {"name_en": "Keo Seima", "name_km": "កែវសីមា"},
        ],
    },
    {
        "code": "ratanakiri",
        "name_en": "Ratanakiri",
        "name_km": "រតនគិរី",
        "lat": 13.7394,
        "lng": 106.9873,
        "districts": [
            {"name_en": "Krong Banlung", "name_km": "ក្រុងបានលុង"},
            {"name_en": "Andoung Meas", "name_km": "អណ្តូងមាស"},
            {"name_en": "Bar Kaev", "name_km": "បរកែវ"},
            {"name_en": "Koun Mom", "name_km": "កូនមុំ"},
            {"name_en": "Lomphat", "name_km": "លំផាត់"},
            {"name_en": "Ou Chum", "name_km": "អូរជុំ"},
            {"name_en": "Ou Ya Dav", "name_km": "អូរយ៉ាដាវ"},
            {"name_en": "Ta Veaeng", "name_km": "តាវែង"},
            {"name_en": "Veun Sai", "name_km": "វើនសៃ"},
        ],
    },
    {
        "code": "tboung_khmum",
        "name_en": "Tboung Khmum",
        "name_km": "ត្បូងឃ្មុំ",
        "lat": 11.8891,
        "lng": 105.8761,
        "districts": [
            {"name_en": "Krong Suong", "name_km": "ក្រុងសួង"},
            {"name_en": "Dambae", "name_km": "ដំបែ"},
            {"name_en": "Krouch Chhmar", "name_km": "ក្រូចឆ្មារ"},
            {"name_en": "Memot", "name_km": "មេមត់"},
            {"name_en": "Ou Reang Ov", "name_km": "អូររាំងឪ"},
            {"name_en": "Ponhea Kraek", "name_km": "ពញាក្រែក"},
            {"name_en": "Tboung Khmum", "name_km": "ត្បូងឃ្មុំ"},
        ],
    },
]

# Quick lookup tables
PROVINCES_BY_CODE = {p["code"]: p for p in CAMBODIA_PROVINCES}
PROVINCES_BY_NAME_EN = {p["name_en"].lower(): p for p in CAMBODIA_PROVINCES}
PROVINCES_BY_NAME_KM = {p["name_km"]: p for p in CAMBODIA_PROVINCES}

FARM_TYPES = [
    {"code": "backyard", "name_en": "Backyard / Free-range", "name_km": "លក្ខណៈគ្រួសារ (លែង)"},
    {"code": "semi_intensive", "name_en": "Semi-intensive", "name_km": "ពាក់កណ្តាលពាណិជ្ជកម្ម"},
    {"code": "commercial_broiler", "name_en": "Commercial Broiler (Meat)", "name_km": "ពាណិជ្ជកម្ម (មាន់សាច់)"},
    {"code": "commercial_layer", "name_en": "Commercial Layer (Eggs)", "name_km": "ពាណិជ្ជកម្ម (មាន់ពង)"},
]

FARM_SCALES = [
    {"code": "<50", "name_en": "< 50 Birds (Small)", "name_km": "< ៥០ ក្បាល (ខ្នាតតូច)"},
    {"code": "50-200", "name_en": "50 - 200 Birds (Medium)", "name_km": "៥០ - ២០០ ក្បាល (មធ្យម)"},
    {"code": "201-1000", "name_en": "201 - 1,000 Birds (Semi-commercial)", "name_km": "២០១ - ១,០០០ ក្បាល (ពាក់កណ្តាលធំ)"},
    {"code": ">1000", "name_en": "> 1,000 Birds (Large Commercial)", "name_km": "> ១,០០០ ក្បាល (កសិដ្ឋានធំ)"},
]


def get_provinces() -> list[dict]:
    """Return all 25 provinces."""
    return CAMBODIA_PROVINCES


def get_province_by_key(val: str | None) -> dict | None:
    """Find province by code, English name, or Khmer name."""
    if not val:
        return None
    val_clean = val.strip()
    val_lower = val_clean.lower()
    if val_lower in PROVINCES_BY_CODE:
        return PROVINCES_BY_CODE[val_lower]
    if val_lower in PROVINCES_BY_NAME_EN:
        return PROVINCES_BY_NAME_EN[val_lower]
    if val_clean in PROVINCES_BY_NAME_KM:
        return PROVINCES_BY_NAME_KM[val_clean]
    # Fuzzy match
    for p in CAMBODIA_PROVINCES:
        if p["name_en"].lower() in val_lower or val_lower in p["name_en"].lower():
            return p
        if p["name_km"] in val_clean or val_clean in p["name_km"]:
            return p
    return None


def get_districts_by_province(province_key: str | None) -> list[dict]:
    """Return district objects for the specified province."""
    prov = get_province_by_key(province_key)
    return prov["districts"] if prov else []


def find_nearest_province(lat: float, lng: float) -> dict:
    """Haversine distance lookup to find the nearest Cambodian province center."""
    best_dist = float("inf")
    best_prov = CAMBODIA_PROVINCES[0]  # default to Phnom Penh

    for p in CAMBODIA_PROVINCES:
        p_lat, p_lng = p["lat"], p["lng"]
        # Haversine
        d_lat = math.radians(p_lat - lat)
        d_lng = math.radians(p_lng - lng)
        a = (
            math.sin(d_lat / 2) ** 2
            + math.cos(math.radians(lat))
            * math.cos(math.radians(p_lat))
            * math.sin(d_lng / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        dist = 6371 * c  # Earth radius in km
        if dist < best_dist:
            best_dist = dist
            best_prov = p

    return best_prov


def normalize_legacy_location(raw_location: str | None) -> tuple[str, str | None]:
    """Parse legacy free-text location into (standard_province_name, district).

    Examples:
        'កំពុងចាម' -> ('Kampong Cham', None)
        'Battam bong' -> ('Battambang', None)
        'Phnom Penh' -> ('Phnom Penh', None)
        'កណ្តាល' -> ('Kandal', None)
    """
    if not raw_location or not raw_location.strip():
        return ("Phnom Penh", None)

    raw = raw_location.strip()

    # Common spelling variations in legacy DB
    legacy_aliases = {
        "កំពុងចាម": "Kampong Cham",
        "កំពង់ចាម": "Kampong Cham",
        "battam bong": "Battambang",
        "battambang": "Battambang",
        "បាត់ដំបង": "Battambang",
        "កណ្តាល": "Kandal",
        "kandal": "Kandal",
        "phnom penh": "Phnom Penh",
        "ភ្នំពេញ": "Phnom Penh",
        "siem reap": "Siem Reap",
        "សៀមរាប": "Siem Reap",
        "takeo": "Takeo",
        "តាកែវ": "Takeo",
        "kampot": "Kampot",
        "កំពត": "Kampot",
    }

    raw_lower = raw.lower()
    for alias, prov_en in legacy_aliases.items():
        if alias in raw_lower or alias in raw:
            return (prov_en, None)

    prov = get_province_by_key(raw)
    if prov:
        return (prov["name_en"], None)

    return ("Phnom Penh", None)
