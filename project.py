from dataset_handler import DatasetHandler

handler = DatasetHandler('Electric_Vehicle_Population_Data.csv')
handler.clean_dataset()

years=sorted(handler._df['Model Year'].unique())
yearly=[]
for year in years:
    byyear=handler._df.loc[handler._df['Model Year'] == year].values
    yearly.append([x[10] for x in byyear])
    
boxplot_data = {
    'xlabel': 'Model Year',
    'ylabel': 'Electric Range',
    'title' : 'Electric Range by Model Year',
    'data': yearly
}
handler.create_boxplot(boxplot_data)

# years=sorted(set(data['Model Year']))
# yearly=[]
# for year in years:
#     byyear=data.loc[data['Model Year'] == year].values
#     yearly.append([x[10] for x in byyear])
# fig = plt.figure()
# ax  = fig.add_subplot(111)
# plt.boxplot(yearly)
# plt.xlabel('Model Year')
# plt.ylabel('Electric Range')
# ax.set_xticklabels(years)
# plt.title(f'Electric Range by Model Year')
# plt.tight_layout()
# # plt.show()

# makes=sorted(set(data['Make']))
# PHEV=[]
# BEV=[]
# for make in makes:
#     bymake=data.loc[data['Make'] == make].values
#     PHEV.append([x[10] for x in bymake if x[8]=="Plug-in Hybrid Electric Vehicle (PHEV)"])
#     BEV.append([x[10] for x in bymake if x[8]=="Battery Electric Vehicle (BEV)"])

# fig = plt.figure()
# ax  = fig.add_subplot(111)
# plt.boxplot(PHEV)
# plt.xlabel('Make')
# plt.ylabel('Electric Range')
# ax.set_xticklabels(makes)
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.title(f'Electric Range by Car Make for PHEV')
# # plt.show()
# fig = plt.figure()
# ax  = fig.add_subplot(111)
# plt.boxplot(BEV)
# plt.xlabel('Make')
# plt.ylabel('Electric Range')
# ax.set_xticklabels(makes)
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.title(f'Electric Range by Car Make for BEV')
# # plt.show()

# fig = plt.figure()
# plt.pie([len(sum(BEV, [])),len(sum(PHEV, []))],labels=["BEV", "PHEV"],autopct='%1.1f%%')
# # plt.show()


# clean=data.loc[data['Clean Alternative Fuel Vehicle (CAFV) Eligibility'] == "Clean Alternative Fuel Vehicle Eligible"].values
# notclean=data.loc[data['Clean Alternative Fuel Vehicle (CAFV) Eligibility'] == "Not eligible due to low battery range"].values
# unknown=data.loc[data['Clean Alternative Fuel Vehicle (CAFV) Eligibility'] == "Eligibility unknown as battery range has not been researched"].values
# fig = plt.figure()
# plt.pie([len(clean),len(notclean),len(unknown)],labels=["Eligiable", "Not Eligible", "Unknown"],autopct='%1.1f%%')
# plt.show()
