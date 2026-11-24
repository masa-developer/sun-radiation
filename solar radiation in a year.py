# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 09:58:43 2026

@author: VK
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# ============================================================
# Theoretical solar energy by latitude
# Horizontal surface, top of atmosphere
# No clouds, no atmosphere, no shading, no PV losses
# ============================================================

G_SC = 1367.0  # Solar constant, W/m²


def daily_extraterrestrial_radiation(latitude_deg, day_of_year):
    """
    Daily solar energy on a horizontal surface at top of atmosphere.

    Returns:
        kWh/m²/day
    """

    lat = np.radians(latitude_deg)
    n = day_of_year

    # Earth-Sun distance correction
    dr = 1.0 + 0.033 * np.cos(2.0 * np.pi * n / 365.0)

    # Solar declination [rad]
    delta = 0.409 * np.sin(2.0 * np.pi * n / 365.0 - 1.39)

    # Sunset hour angle
    x = -np.tan(lat) * np.tan(delta)
    x = np.clip(x, -1.0, 1.0)
    omega_s = np.arccos(x)

    # Daily radiation, J/m²/day
    H0_J = (
        24.0 * 3600.0 / np.pi
        * G_SC
        * dr
        * (
            omega_s * np.sin(lat) * np.sin(delta)
            + np.cos(lat) * np.cos(delta) * np.sin(omega_s)
        )
    )

    # Convert J/m²/day to kWh/m²/day
    H0_kWh = H0_J / 3.6e6

    return H0_kWh


# ============================================================
# Latitudes to compare
# ============================================================

latitudes = np.arange(0, 71, 5)
days = np.arange(1, 366)

# Non-leap-year date axis
start_date = datetime(2024, 1, 1)
dates = np.array([start_date + timedelta(days=int(d - 1)) for d in days])

annual_energy = []

# ============================================================
# Figure 1: Daily solar energy through the year
# Month-based x-axis
# ============================================================

plt.figure(figsize=(12, 7))

for lat in latitudes:

    daily_energy = np.array([
        daily_extraterrestrial_radiation(lat, d)
        for d in days
    ])

    annual_energy.append(np.sum(daily_energy))

    plt.plot(dates, daily_energy, label=f"{lat}°N")

plt.xlim(datetime(2024, 1, 1), datetime(2024, 12, 31))
plt.ylim(0, 30)

plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))

plt.xlabel("Month")
plt.ylabel("Daily solar energy (kWh/m²/day)")
plt.title("Theoretical daily solar energy at different latitudes")
plt.grid(True)
plt.legend(ncol=3)
plt.tight_layout()


# ============================================================
# Figure 2: Annual total energy vs latitude
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(latitudes, annual_energy, 'o-')

plt.xlim(0, 70)
plt.ylim(0, 7000)

plt.xlabel("Latitude (°N)")
plt.ylabel("Annual solar energy (kWh/m²/year)")
plt.title("Theoretical annual solar energy vs latitude")
plt.grid(True)
plt.tight_layout()


# ============================================================
# Print table
# ============================================================

print()
print("Annual theoretical solar energy")
print("-----------------------------------")
print(" Latitude      Energy")
print("   (°N)      (kWh/m²/year)")
print("-----------------------------------")

for lat, E in zip(latitudes, annual_energy):
    print(f"{lat:5.0f}         {E:8.1f}")

plt.show()