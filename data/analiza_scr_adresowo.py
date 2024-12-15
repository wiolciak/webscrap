import pandas as pd
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from tabulate import tabulate
# mpl.rcParams['axes.formatter.useoffset'] = False  # Wyłącz przesunięcie osi
# mpl.rcParams['axes.formatter.use_locale'] = False  # Wyłącz notację naukową
# mpl.rcParams['axes.formatter.use_mathtext'] = False  # Wyłącz format naukowy

data_folder = Path(__file__).resolve().parent
df = pd.read_csv("listings.csv")
# df = pd.read_csv("C:\\Users\\wmwsz\\OneDrive\\Desktop\\SDA\\M5L4\\data-science\\listings.csv")

# print(df.dtypes)

# 1. filtrowanie np dla mieszkań dwupokojowych, cena poniżej 650000, pow.40:
# filtered_room_2 = df[(df['room'] == 2) & (df['price'] <= 650000) & (df['pow'] >= 40)]
# print(filtered_room_2)

# 2. średnia cena za m2
# average_price_per_m2 = df['price_m2'].mean().round(2)
# print(f"Średnia cena za m²: {average_price_per_m2} zł")

# 3. sortowanie danych po cenie za m2 od najmniejszej 
# df_sorted = df.sort_values(by = ['price_m2']).head(10)# ascending=False sortuje od największej do najmniejszej
# print(df_sorted)


# 4. zapytanie dla użytkownika
# def filter_and_display(df):
#     pow_min = float(input("Podaj minimalną powierzchnię w metrach kwadratowych: "))
#     price_max = float(input("Podaj maksymalną cenę w złotych: "))
#     room = int(input("Podaj liczbę pokoi: "))

#     filtered_df = df[(df['room'] == room) & (df['price'] <= price_max) & (df['pow'] >= pow_min)]
#     unique_df = filtered_df.drop_duplicates()
#     print(tabulate(unique_df, headers='keys', tablefmt='pretty'))
#     return unique_df
# filtered_df = filter_and_display(df)

# 5. grupowanie po dzielnicach i obliczanie średniej ceny za m2 dla każdej dzielnicy na podstawie ogłoszeń

def get_filtered_district(title):
    part = title.split(' ', 1) 
    if len(part) > 1:
        return part[1]
    # else:
    #     return "Brak danych o dzilnicach"
    # jest to potrzebne do tego by określić czy są dane bez dzilnic
df['filtered_district'] = df['title'].apply(get_filtered_district)
# # # print(df['filtered_district'].unique())
      
title_gruped = df.groupby('filtered_district')
avg_price_m2_for_title = title_gruped['price_m2'].mean().round(2)
sorted_avg_price_m2_for_title = avg_price_m2_for_title.sort_values(ascending=False)

plt.figure(figsize=(15, 6))
sorted_avg_price_m2_for_title.sort_values(ascending=False)
colors = plt.cm.autumn(np.linspace(0, 1, len(sorted_avg_price_m2_for_title)))
ax = sorted_avg_price_m2_for_title.plot(kind='bar', color=colors, edgecolor='black', linewidth=1.5, label='Średnia cena za m²')

plt.title('Średnia cena za m² wg dzielnic w mieście Kraków', fontsize=16, weight='bold')
plt.xlabel('Dzielnice w mieście Kraków')
plt.ylabel('Średnia cena za m² (zł)')
plt.xticks(rotation=45, ha='right') # Obrócenie etykiet osi X dla lepszej czytelności
plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
ax.set_facecolor('lightgray')
plt.tight_layout()
plt.show()


# 6. ceny mieszkań na podstwie ogloszeń uśrenione dla dzielnic
avg_price_for_title = title_gruped['price'].mean().round(2)
sort_highest = avg_price_for_title.sort_values(ascending=False)
sort_lowest = avg_price_for_title.sort_values(ascending=True)
highest_price_title = sort_highest.idxmax()
lowest_price_title = sort_lowest.idxmin()

# print(f"Dzielnica z najwyższymi cenami: {highest_price_title} - {sort_highest.max()} zł")
# print(f"Dzielnica z najniższymi cenami: {lowest_price_title} - {sort_lowest.min()} zł")


# plt.figure(figsize=(20, 6))
sorted_avg_price_m2_for_title.sort_values(ascending=False)
colors = plt.cm.autumn(np.linspace(0, 1, len(sorted_avg_price_m2_for_title)))
# ax = sorted_avg_price_m2_for_title.plot(kind='bar', color=colors, edgecolor='black', linewidth=1.5, label='Średnia cena za m²')



plt.figure(figsize=(15, 6))
colors = plt.cm.winter(np.linspace(0, 1, len(sort_highest)))
ax=sort_highest.plot(kind='bar', color=colors, edgecolor='black',linewidth=1.5, label=('Średnie zestawienie cen'))
formatter = ticker.ScalarFormatter()
formatter.set_scientific(False)
ax.yaxis.set_major_formatter(formatter)
y_ticks = [i for i in range(250000, 2250001, 250000)]
ax.set_yticks(y_ticks)
ax.set_yticklabels([f'{tick:.0f} zł' for tick in y_ticks])


plt.title("Średnie ceny mieszkań w Krakowie wg dzielnic w mieście Kraków", fontsize=16, weight='bold')
plt.xlabel("Dzielnice w mieście Kraków")
plt.ylabel("Średnia cena (zł)")
plt.xticks(rotation=45, ha='right')
plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.5)  # Rotate labels for better readability
plt.tight_layout()  # Adjust layout
plt.savefig('output_plot.png', bbox_inches='tight')
ax.set_facecolor('lightgray')
plt.show()


# # 7. ilość pokoi w stosunku do mieszkań 
# unique_rooms = df['room'].unique()
rooms_counts = df['room'].value_counts().sort_index()
# print(f"Unikalne liczby pokoi: {unique_rooms}")
# print(f"Liczba mieszkań dla każdego typu pokoju:\n{rooms_counts}")
plt.figure(figsize=(8, 6))
plt.plot(rooms_counts.index, rooms_counts.values, marker='p', linestyle='-', color='darkgrey', label='Liczba mieszkań', linewidth=2.5, markersize=17, markerfacecolor='white', markeredgewidth=2, markeredgecolor="blue")
labels = rooms_counts.values
for i in range(len(labels)):
    label = labels[i]
    plt.text(
        rooms_counts.index[i], rooms_counts.values[i], str(label), ha='center', va='center', fontsize=8, color='blue' )
plt.title('Liczba mieszkań w zależności od liczby pokoi', fontsize=16, weight='bold')
plt.xlabel('Liczba pokoi')
plt.xticks(rooms_counts.index) 
plt.ylabel('Liczba mieszkań')
plt.grid(True, linestyle='--', alpha=0.9)
plt.legend()
plt.show()

# 8. śrenia powierzchnia mieszkań w dzielnicach KRakowa

df['filtered_district'] = df['title'].apply(get_filtered_district)
avg_pow_filtered_district = df.groupby('filtered_district')['pow'].mean().reset_index()
# print(avg_pow_filtered_district)
x = avg_pow_filtered_district['filtered_district']
y = avg_pow_filtered_district['pow']

plt.figure(figsize=(10, 6)) 
plt.title('Średnia powierzchnia mieszkań w dzielnicach', fontsize = 16, fontweight = 'bold')
plt.xlabel('Dzielnica')
plt.ylabel('Średnia powierzchnia (m²)') 
plt.stem(x, y, markerfmt='o', basefmt=' ', linefmt='orange')
plt.grid(which='both', linestyle='--', linewidth=0.5) 
plt.xticks(rotation=60)
plt.tight_layout()
plt.show()

# 9.  wykres punktowy (scatter plot) rozkładu ceny względem powierzchni
plt.figure(figsize=(15, 6))
subset = df.sample(100)
plt.scatter(subset['price_m2'], subset['price'], color='red', edgecolor='red', alpha=0.2, s = 20)
plt.title("Rozkład ceny za m² względem  ceny całkowitej", fontsize = 16, fontweight = 'bold')
plt.xlabel('Cena za m²')
plt.ylabel('Cena')

formatter = ticker.ScalarFormatter()
formatter.set_scientific(False)
plt.gca().yaxis.set_major_formatter(formatter)
plt.gca().patch.set_facecolor('lightgrey')

y_ticks = [i for i in range(250000, 4000001, 250000)]
plt.gca().set_yticks(y_ticks)
plt.gca().set_yticklabels([f'{tick:.0f} zł' for tick in y_ticks], rotation=45, fontsize=10) # zrób bez eltykiedty zł

x = df['price_m2']
y = df['price']
line = np.polyfit(x, y, 1)
trendline = np.poly1d(line)
plt.plot(x, trendline(x), color='yellow', linewidth=2, label='Liczba trendu: y={}x + {}'.format(line[0], line[1]))

plt.legend()
plt.tight_layout()
plt.show()

# 10. cena za m2 względem powierzchni
plt.figure(figsize=(15, 6))
subset = df.sample(100)
plt.scatter(subset['pow'], subset['price_m2'], color='blue', alpha=0.3, s = 20)
plt.title("Cena m² w zależności od powierzchni", fontsize=16, fontweight='bold')
plt.xlabel("Powierzchnia (m²)")
plt.ylabel("Cena m² (zł)")
plt.gca().patch.set_facecolor('lightgrey')

x = df['pow']
y = df['price_m2']
line_m2_t = np.polyfit(x, y, 1)  # Dopasowanie liniowe (stopień 1)
trendline = np.poly1d(line_m2_t)
plt.plot(x, trendline(x), color='orange', linewidth=1,  label=f'Linia trendu: y={line_m2_t[0]:.2f}x + {line_m2_t[1]:.2f}')
plt.legend()
plt.tight_layout()
plt.show()


# # 11. Udział pokoi w zbiorze mieszkań
room_counts = df['room'].value_counts(ascending=True)
explode = (0, 0, 0.1, 0)  
colors = ['gold', 'lightcoral', 'lightskyblue', 'mediumseagreen']

plt.figure(figsize=(8, 8))
plt.pie(
    room_counts, explode=explode,autopct='%1.1f%%', startangle=140, colors=colors, shadow=True)

plt.legend(room_counts.index, title="Liczba pokoi", loc="center left", bbox_to_anchor=(0.9, 0, 0.5, 1))
plt.title("Udział liczby pokoi w zbiorze mieszkań", fontsize=16, fontweight='bold')
plt.show()


# # 12. Udział dzielnic w zbiorze danych

room_distribution = df.groupby('title')['room'].value_counts().unstack().fillna(0)
# print(room_distribution)
room_distribution.plot(kind='barh', stacked=True, figsize=(12, 8), colormap='viridis')

plt.title('Rozkład liczby mieszkań w zależności od liczby pokoi w różnych dzielnicach',fontsize=16, weight='bold')
plt.ylabel('Dzielnice')
plt.xlabel('Liczba mieszkań')
plt.grid(axis='x',linestyle='--', alpha=0.7)
plt.legend(title='Liczba pokoi', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()


















