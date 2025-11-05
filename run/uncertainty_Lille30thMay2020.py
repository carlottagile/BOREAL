# %% IMPORTS 
import os
import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt


# %% FILE PATHS 
# VSD_directory = '/Users/dada/Desktop/TFM/EARLINET_Database/LILLE_30_05_2020/Retrieval_Uncertainty/VSDs_Lille30thMay2020'
# DATA_directory = '/Users/dada/Desktop/TFM/EARLINET_Database/LILLE_30_05_2020/Retrieval_Uncertainty/DATA_Lille30thMay2020'

VSD_directory = '/Users/dada/Desktop/TFM/EARLINET_Database/LILLE_30_05_2020/Retrieval_Uncertainty/VSDs_Lille30thMay2020_very_small_error'
DATA_directory = '/Users/dada/Desktop/TFM/EARLINET_Database/LILLE_30_05_2020/Retrieval_Uncertainty/DATA_Lille30thMay2020_very_small_error'

DATA_realization00_path = '/Users/dada/Desktop/TFM/EARLINET_Database/LILLE_30_05_2020/Retrieval_Uncertainty/DATA_Lille30thMay2020_very_small_error/Realization_00.csv'
VSD_realization00_path = '/Users/dada/Desktop/TFM/EARLINET_Database/LILLE_30_05_2020/Retrieval_Uncertainty/VSDs_Lille30thMay2020_very_small_error/Realization_00.csv'

DATA_3times_path = '/Users/dada/Documents/Selenium/outputs/DATA/Lille_3times_std_dev.csv'
VSD_3times_path = '/Users/dada/Documents/Selenium/outputs/VSDs/Lille_3times_std_dev.csv'

# %% READING FILES 

# Call x, one of the VSDs and sigma the std of that VSD
# We have 100 pairs (x, std_x) 
# Call E(x) = VSD_mean_VSD and SD(x) = random error
# Call E(sigma) = systematic error 
# Find SD(sigma)

# Reading Realization 00 (IS) VSD
df_00 = pd.read_csv(VSD_realization00_path)
VSD_IS = np.array(df_00['VSD(um^3/cm^3)'])
VSD_std_IS = np.array(df_00['VSD_std(um^3/cm^3)'])
radii = np.array(df_00['r(um)'])

# Reading "3 times std_dev" VSD
df_3times = pd.read_csv(VSD_3times_path)
VSD_3times = np.array(df_3times['VSD(um^3/cm^3)'])
VSD_std_3times = np.array(df_3times['VSD_std(um^3/cm^3)'])

# Reading 100 realizations
# Creating list of file paths 
DATA_file_list = sorted([os.path.join(DATA_directory, f) for f in os.listdir(DATA_directory) 
              if os.path.isfile(os.path.join(DATA_directory, f))])
VSD_file_list = sorted([os.path.join(VSD_directory, f) for f in os.listdir(VSD_directory) 
              if os.path.isfile(os.path.join(VSD_directory, f))])

VSDs = []
VSD_stds = []
file_names = []
for file_path in VSD_file_list[1:]:
    file_name = os.path.basename(file_path)
    df = pd.read_csv(file_path)
    vsd = df['VSD(um^3/cm^3)']
    vsd = np.array(vsd)
    VSDs.append(vsd)
    vsd_std = df['VSD_std(um^3/cm^3)']
    vsd_std = np.array(vsd_std)
    VSD_stds.append(vsd_std)
    file_names.append(file_name)

VSDs = np.array(VSDs)
VSD_stds = np.array(VSD_stds)

VSDs_df = pd.DataFrame(
    data=VSDs,
    index=file_names,
)

VSDs_std_df = pd.DataFrame(
    data=VSD_stds,
    index=file_names)

# Calculating mean of VSD of 100 realizations 
mean_VSD = np.array(VSDs_df.mean(axis=0))

# Calculating std dev of 100 realizations (random error)
std_VSD = np.array(VSDs_df.std(axis=0)) 

std_VSD_std = np.array(VSDs_std_df.std(axis=0))

VSDs_df.reset_index(inplace=True)

systematic_error = np.array(VSDs_std_df.mean(axis=0)) 


plt.figure(figsize=(12, 6))
for i, vsd in enumerate(VSDs):
    plt.plot(radii, vsd, marker='o', linestyle='-', color='r', label='VSD calculated')
    print(i, vsd)
plt.plot(radii, VSDs[5,:], marker='o', linestyle='-', color='black', label='VSD calculated')
plt.xscale('log')



# %% Plot VSD from IS vs VSD calculated from realizations 

# Plot of VSDs 
plt.figure(figsize=(12, 6))
plt.plot(radii, VSD_3times, marker='x', linestyle='--', color='b', label='Original VSD')
plt.plot(radii, mean_VSD, marker='o', linestyle='-', color='r', label='VSD calculated')
plt.xscale('log')
plt.title('Plot of Volume Size Distribution')
plt.xlabel('Radius (um)')
plt.ylabel('VSD Values (um^3/cm^3)')
plt.grid(True)
plt.legend()
plt.show()

difference = mean_VSD - VSD_3times 

# Plot of E(x) - Original VSD 
plt.figure(figsize=(12, 6))
plt.plot(radii, difference, marker='x', linestyle='--', color='b')
plt.xscale('log')
plt.title(r'Plot of $E(\overline{x})$ - Original VSD')
plt.xlabel(r'Radius ($\mu$m)')
plt.ylabel(r'VSD Values ($\mu$m$^3$/cm$^3$)')
plt.grid(True)
plt.show()

# Plot of VSDs con error bars 
plt.figure(figsize=(12, 6))
plt.errorbar(radii, VSD_3times, yerr=VSD_std_3times, marker='x', linestyle='--', color='b', 
             label='Original VSD', capsize=3, zorder=1)
plt.xscale('log')
plt.title('Plot of Volume Size Distribution with Error Bars (Original VSD and Original VSD STD)')
plt.xlabel('Radius (um)')
plt.ylabel('VSD Values (um^3/cm^3)')
plt.grid(True)
plt.legend()
plt.show()

# Plot of the VSD derived from realizations with error bars 
plt.figure(figsize=(12, 6))
plt.errorbar(radii, mean_VSD, yerr=std_VSD, marker='o', linestyle='-', color='r',
             label='VSD calculated', capsize=3)

plt.xscale('log')
plt.title('Plot of Volume Size Distribution with Error Bars (Error Bars from Equation 3)')
plt.xlabel('Radius (um)')
plt.ylabel('VSD Values (um^3/cm^3)')
plt.ylim([-1,14])
plt.grid(True)
plt.legend()
plt.show()

# Plot of the VSD derived from realizations with error bars 
plt.figure(figsize=(12, 6))
plt.errorbar(radii, mean_VSD, yerr=systematic_error, marker='o', linestyle='-', color='g',
             label='VSD calculated', capsize=3)

plt.xscale('log')
plt.title('Plot of Volume Size Distribution with Error Bars (Error Bars from Equation 2)')
plt.xlabel('Radius (um)')
plt.ylabel('VSD Values (um^3/cm^3)')
plt.ylim([-1,14])
plt.grid(True)
plt.legend()
plt.show()


# Plot of the error bars from BOREAL 
plt.figure(figsize=(12,6))
plt.plot(radii, VSD_std_3times, marker='x', linestyle='--', color='b', label='Original VSD STD')
plt.xscale('log')
plt.title('Plot of the Original Standard Deviation (Original VSD STD)')
plt.xlabel('Radius (um)')
plt.ylabel('VSD STD Values (um^3/cm^3)')
plt.ylim([-1,2])
plt.grid(True)
plt.legend()
plt.show()

# Plot of the error bars from BOREAL 
plt.figure(figsize=(12,6))
plt.plot(radii, std_VSD, marker='x', linestyle='-', color='r', label='VSD STD from Equation 3')
plt.xscale('log')
plt.title('Plot of the Standard Deviation ofrom Equation 3')
plt.xlabel('Radius (um)')
plt.ylabel('VSD STD Values (um^3/cm^3)')
plt.ylim([-1,2])
plt.grid(True)
plt.legend()
plt.show()

# Plot of the error bars from BOREAL 
plt.figure(figsize=(12,6))
plt.plot(radii, systematic_error, marker='x', linestyle=':', color='g', label='VSD STD from Equation 2')
plt.xscale('log')
plt.title('Plot of the Standard Deviation from Equation 2')
plt.xlabel('Radius (um)')
plt.ylabel('VSD STD Values (um^3/cm^3)')
plt.ylim([-1,2])
plt.grid(True)
plt.legend()
plt.show()

# Plot of the standard deviation of the standard deviations of the VSDs
plt.figure(figsize=(12,6))
plt.plot(radii, std_VSD_std, marker='x', linestyle=':', color='black', label='STD of VSD STD')
plt.xscale('log')
plt.title('Plot of the Standard Deviation of the VSDs')
plt.xlabel('Radius (um)')
plt.ylabel('VSD STD Values (um^3/cm^3)')
plt.ylim([-1,2])
plt.grid(True)
plt.legend()
plt.show()
# %% CRI Analysis 

# Realization 00 reading of CRI 
df_data_00 = pd.read_csv(DATA_realization00_path)
df_data_00.columns
mR_00 = np.array(df_data_00['mR'])
mR_std_00 = np.array(df_data_00['mR.1'])
mI_00 = np.array(df_data_00['mI'])
mI_std_00 = np.array(df_data_00['mI.1'])
IS_00 = np.array(df_data_00['IS'])

# "3 times" reading of CRI
df_data_3times = pd.read_csv(DATA_3times_path)
mR_3times = np.array(df_data_3times['mR'])
mR_std_3times = np.array(df_data_3times['mR.1'])
mI_3times = np.array(df_data_3times['mI'])
mI_std_3times = np.array(df_data_3times['mI.1'])
IS_3times = np.array(df_data_3times['IS'])

# 100 Realization s reading of CRI
data_list = []

# Other 100 realizations 
for file_path in DATA_file_list[1:]:
    df = pd.read_csv(file_path)
    
    # Extract mR and mR_std 
    mR = float(df.iloc[1, df.columns.get_loc('mR')] )
    mR_std = float(df.iloc[1, df.columns.get_loc('mR.1')])
    
    # Extract mI and mI_std
    mI = float(df.iloc[1, df.columns.get_loc('mI')])
    mI_std = float(df.iloc[1, df.columns.get_loc('mI.1')])
    
    # Extract IS
    IS = int(df.iloc[1,df.columns.get_loc('IS')])
    
    # Append to list
    data_list.append([mR, mR_std, mI, mI_std, IS])
    
data_list = np.array(data_list)

columns = ['mR', 'mR_std', 'mI', 'mI_std', 'IS']

data_df = pd.DataFrame(
    data = data_list,
    columns=columns,
    index=file_names)

mean_CRI = np.array(data_df.mean(axis=0))
std_CRI = np.array(data_df.std(axis=0))
mR_mean_calculated = mean_CRI[0]
mR_std_calculated = mean_CRI[1]
mI_mean_calculated = mean_CRI[2]
mI_std_calculated = mean_CRI[3]
mean_IS_calculated = mean_CRI[4]
std_IS_calculated = std_CRI[4]


random_CRI = np.array(data_df.std(axis=0))

random_mR_std = random_CRI[0]
random_mI_std = random_CRI[2]

# %% Plot of the CRI
print(f"mR (mean) from IS: {mR_00[1]}")
print(f"mR (mean) calculated: {mR_mean_calculated:.3f}")
print(f"mR (mean) 3-times trial: {mR_3times[1]}\n")

print(f"mR (std) from IS: {mR_std_00[1]}")
print(f"mR (std) calculated: {mR_std_calculated:.3f}")
print(f"mR (std) 3-times trial: {mR_std_3times[1]}\n")
print(f"mR (std) random: {random_mR_std:.3f}")

print(f"mI (mean) from IS: {mI_00[1]}")
print(f"mI (mean) calculated: {mI_mean_calculated:.3f}")
print(f"mI (mean) 3-times trial: {mI_3times[1]}\n")

print(f"mI (std) from IS: {mI_std_00[1]}")
print(f"mI (std) calculated: {mI_std_calculated:.3f}")
print(f"mI (std) 3-times trial: {mI_std_3times[1]}\n")
print(f"mI (std) random: {random_mI_std:.3f}")

# Plot of the mean value of the real part of the CRI
plt.figure(figsize=(12, 6))
plt.plot(float(mR_00[1]), marker='x', linestyle='--', color='b', label='mR from IS')
plt.plot(mR_mean_calculated, marker='o', linestyle='-', color='r', label='mR calculated')
plt.plot(float(mR_3times[1]), marker='s', linestyle=':', color='g', label='3-times std')
plt.title('Plot of Real Part of CRI (Mean Value)')
plt.ylabel('mR (mean)')
plt.grid(True)
plt.legend()
plt.show()

# Plot of the mean value of the imaginary part of the CRI
plt.figure(figsize=(12, 6))
plt.plot(float(mI_00[1]), marker='x', linestyle='--', color='b', label='mI from IS')
plt.plot(mI_mean_calculated, marker='o', linestyle='-', color='r', label='mI calculated')
plt.plot(float(mI_3times[1]), marker='s', linestyle=':', color='g', label='3-times std')
plt.title('Plot of Imaginary Part of CRI (Mean Value)')
plt.ylabel('mI (mean)')
plt.grid(True)
plt.legend()
plt.show()

# %%
# Plot if IS as a function of the realizations 
data_df2 = data_df.copy()
data_df2.reset_index(inplace=True)
plt.figure(figsize=(12,6))
plt.scatter(data_df2.index, data_df2['IS'], s=20, color='black', label='IS for each realization')
plt.axhline(y=mean_IS_calculated, color='b', linestyle='--', label=f'Mean of ISs = {mean_IS_calculated}')
plt.axhline(y=IS_3times[-1], linestyle='-', color='r', label=f'Original VSD IS = {IS_3times[-1]}')
plt.axhline(y=mean_IS_calculated+(std_IS_calculated/2), color='black', linestyle=':', label='Mean of ISs + STD/2')
plt.axhline(y=mean_IS_calculated-(std_IS_calculated/2), color='black', linestyle=':', label='Mean of ISs - STD/2')
plt.title('Plot of the IS of the Realizations')
plt.xlabel('Realizations')
plt.ylabel('IS')
plt.ylim([-0,10])
# plt.grid(True)
plt.legend()
plt.show()





