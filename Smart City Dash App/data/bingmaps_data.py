## ----------------------------------------------------------------- Webcams ---
pp_webcams = [
   {
      "location": [
         48.799545,
         9.798246
      ],
      "options": {
         "anchor": [13, 5],
         "icon": "webcam"
      },
      "metadata": {
         "id": "webcam_01",
         "title": "Marktplatz",
         "description": "Webcam Marktplatz"
      }
   },
   {
      "location": [
         48.802967,
         9.806969
      ],
      "options": {
         "anchor": [8, 8],
         "icon": "webcam"
      },
      "metadata": {
         "id": "webcam_02",
         "title": "Tunneleingang Ost",
         "description": "Webcam Tunneleingang Ost"
      }
   }
]
## --------------------------------------------------------- Webcam Polygons---
pg_webcams = [
{
    "method": 'complex',
    "points": [
        [48.799545, 9.798246], ## webcam #1
        [48.799654, 9.797749], [48.800071, 9.797219], [48.800139, 9.797399], [48.801250, 9.796637], ## view limit east
        [48.801351, 9.797035], [48.800049, 9.797862], [48.800047, 9.797966], [48.799708, 9.798355], ## view limit west
        [48.799545, 9.798246]  ## webcam #1
    ],
    "options": { "fillColor": '#C8D6B990', "strokeThickness": 0.5, "strokeColor": '#C23B23' }
}, {
    "method": 'complex',
    "points": [
        [48.802967, 9.806969], ## webcam #2 angle east (tunnel entrance)
        [48.802488, 9.805902], [48.802709, 9.805451], [48.802426, 9.803673],  ## view limit east
        [48.802610, 9.803576], [48.802764, 9.804898], [48.803121, 9.805746], ## view limit north
        [48.802967, 9.806969]  ## webcam #2 angle east (tunnel entrance)
    ],
    "options": { "fillColor": '#8FC1A990', "strokeThickness": 0.5, "strokeColor": '#C23B23' }
}, {
    "method": 'complex',
    "points": [
        [48.802967, 9.806969], ## webcam #2 angle north (aldi sued)
        [48.803121, 9.805746], [48.804427, 9.807225], ## view limit north
        [48.802967, 9.806969]  ## webcam #2 angle north (aldi sued)
    ],
    "options": { "fillColor": '#C8D6B990', "strokeThickness": 0.5, "strokeColor": '#C23B23' }
}, {
    "method": 'complex',
    "points": [
        [48.802967, 9.806969], ## webcam #2 angle north-west (pedestrian bridge)
        [48.804427, 9.807225], [48.804148, 9.808011], ## view limit north
        [48.803629, 9.808236], [48.803421, 9.808016], ## view limit south
        [48.802967, 9.806969]  ## webcam #2 angle north-west (pedestrian bridge)
    ],
    "options": { "fillColor": '#8FC1A990', "strokeThickness": 0.5, "strokeColor": '#C23B23' }
}
]
## ----------------------------------------------------------------- Parking ---
pp_parking = [
   {
      "location": [
         48.801346,
         9.800518
      ],
      "options": {
         "icon": "parkingLotSign"
      },
      "metadata": {
         "id": "parking_01",
         "title": "City Center",
         "description": "P1 Parkhaus City Center"
      }
   },
   {
      "location": [
         48.798172,
         9.794074
      ],
      "options": {
         "icon": "parkingLotSign"
      },
      "metadata": {
         "id": "parking_02",
         "title": "Parler Markt",
         "description": "P2 Parkhaus Parler Markt"
      }
   },
   {
      "location": [
         48.7989,
         9.790356
      ],
      "options": {
         "icon": "parkingLotSign"
      },
      "metadata": {
         "id": "parking_03",
         "title": "Stadtgarten",
         "description": "P3 Tiefgarage Congresszentrum Stadtgarten"
      }
   },
   {
      "location": [
         48.801594,
         9.793357
      ],
      "options": {
         "icon": "parkingLotSign"
      },
      "metadata": {
         "id": "parking_04",
         "title": "Rems Galerie",
         "description": "P4 Parkplatz Rems Galerie"
      }
   },
   {
      "location": [
         48.803207,
         9.799902
      ],
      "options": {
         "icon": "parkingLotSign"
      },
      "metadata": {
         "id": "parking_05",
         "title": "Rems-Deck",
         "description": "P5 Parkhaus Rems-Deck"
      }
   },
   {
      "location": [
         48.801327,
         9.7903
      ],
      "options": {
         "icon": "parkingLotSign"
      },
      "metadata": {
         "id": "parking_06",
         "title": "Fehrle-Parkhaus",
         "description": "P6 Fehrle-Parkhaus"
      }
   }
]
## --------------------------------------------------------------- Roadworks ---
pp_roadworks = [
{
   "location": [48.803167, 9.826530],
   "options": {
      "icon": "roadworksSign"
   },
   "metadata": {
      "id": "rw_00c18301",
      "address": "B29 Aalener Straße - to Aalen",
      "start": "15.08.2020",
      "end": "25.08.2020",
      "measure": "Streetworks",
      "description": "Ironworks, Lining and resurfacing works. These works will be for a duration of approx. 10 days in the dates stated. The works will commence under day time or night time closures. Advance warnings signs will be erected 2 weeks before works commence.",
      "obstruction": {
            "lanes": "Full closures"
      }
   }
},
{
   "location": [48.795094, 9.803745],
   "options": {
      "icon": "roadworksSign"
   },
   "metadata": {
      "id": "rw_5f9ff192",
      "address": "Klarenbergstraße 46",
      "start": "08.02.2020",
      "end": "03.2020",
      "measure": "Poly duct installation",
      "description": "Install 6m of 1 way poly duct in Footway, provide 1 core drill(s) into jointbox or building"
   }
},
{
   "location": [48.80091, 9.795406],
   "options": {
      "icon": "roadworksSign"
   },
   "metadata": {
      "id": "rw_30a22913",
      "address": "Waisenhausgasse 2-17",
      "start": "21.04.2019",
      "end": "15.04.2020",
      "estimated": "05.2020",
      "measure": "Excavation works",
      "phase": "T2",
      "description": "Excavate in the CW to repair leak on 30cm water main, complete reinstatement",
      "obstruction": {
            "speed_limit": 30,
            "lanes": 1
      }
   }
},
{
   "location": [48.802159, 9.808250],
   "options": {
      "icon": "roadworksSign"
   },
   "metadata": {
      "id": "rw_4673c9c0",
      "address": "Möhlerstraße 2-18",
      "start": "11.06.2019",
      "end": "12.11.2019",
      "estimated": "05.2020",
      "measure": "Minor Non-Excavation Works",
      "description": "South lane closure to be installed using full chapter 8 signage and barriers. Cherry picker to access telecoms antenna for testing/maintenance works.",
      "obstruction": {
            "speed_limit": 30,
            "lanes": 1
      }
   }
},
{
    "location": [48.795857, 9.798475],
    "options": {
       "icon": "roadworksSign"
    },
    "metadata": {
       "id": "rw_9383b281",
       "address": "Intersection Parlerstraße/Waldstetter Gasse",
       "start": "16.08.2019",
       "end": "17.08.2019",
       "measure": "Traffic light repair",
       "description": "Due to heavy winds minor repairs on have to be made. Temporary self operation traffic light system is used to handle traffic.",
       "obstruction": {
            "speed_limit": 20,
            "lanes": 1
       }
    }
},
{
    "location": [48.803780, 9.818282],
    "options": {
       "icon": "roadworksSign"
    },
    "metadata": {
       "id": "rw_4f5c2412",
       "address": "Klosterberg 2",
       "start": "05.11.2019",
       "end": "18.12.2019",
       "measure": "Cable installation",
       "description": "Locate tee in footway for customer."
    }
},
{
    "location": [48.781243, 9.796218],
    "options": {
       "icon": "roadworksSign"
    },
    "metadata": {
       "id": "rw_04512462",
       "address": "Einhornstraße between Laawiesenweg and Kastellstraße",
       "start": "01.11.2019",
       "end": "16.12.2019",
       "measure": "Streetworks",
       "description": "Resurfacing and closing of various potholes, as well as closing cracks that have formed.",
       "obstruction": {
            "speed_limit": 20,
            "lanes": 1
       }
    }
},
{
    "location": [48.795526, 9.811433],
    "options": {
       "icon": "roadworksSign"
    },
    "metadata": {
       "id": "rw_48b3b903",
       "address": "Hardtstraße 54",
       "start": "12.08.2019",
       "end": "03.09.2019",
       "measure": "Cable repair",
       "description": "Maintenance dig in footway of resident to expose and repair out of service telecoms cable."
    }
},
{
    "location": [48.793231, 9.781904],
    "options": {
       "icon": "roadworksSign"
    },
    "metadata": {
       "id": "rw_ab91029c",
       "address": "Auf den Hochwiesen 1-17",
       "start": "01.10.2019",
       "end": "02.02.2020",
       "measure": "Streetworks",
       "description": "Installation of Ducting and Chambers for UTMC. Resurfacing, Footway Reconstruction and Drainage Works.",
       "obstruction": {
            "speed_limit": 30,
            "lanes": "Total road section closure"
       }
    }
},
{
    "location": [48.796799, 9.792230],
    "options": {
       "icon": "roadworksSign"
    },
    "metadata": {
       "id": "rw_5318a843",
       "address": "Lessingstraße 2",
       "start": "21.11.2019",
       "end": "05.12.2019",
       "measure": "Streetworks",
       "description": "Retrofitting street lamp, new luminous efficiency of 120 lm/w. Additional transfer of DNO service and removing of old stump.",
       "obstruction": {
            "speed_limit": 30,
            "lanes": 1
       }
    }
}
]
## ----------------------------------------------------- Roadworks Polylines ---
pl_roadworks = [
  {     ## rw_00c18301 (Aalener Straße) || east -> west
    "points": [[48.802710, 9.822131], [48.803067, 9.826530], [48.803357, 9.830274]],
    "options": { "strokeColor": "#E50000", "strokeThickness": 8 }
  }, {  ## rw_30a22913 (Waisenhausgasse) || east -> west
    "points": [[48.800853, 9.795262], [48.800915, 9.795377], [48.801111, 9.795661], [48.801256, 9.795902]],
    "options": { "strokeColor": "#E50000", "strokeThickness": 7 }
  }, {  ## rw_4673c9c0 (Möhlerstraße) || east -> west
    "points": [[48.801854, 9.807743], [48.802095, 9.808327], [48.802173, 9.808609], [48.802219, 9.809132]],
    "options": { "strokeColor": "#E50000", "strokeThickness": 7 }
  }, {  ## rw_04512462 (Einhornstraße) || north -> south
    "points": [[48.783023, 9.797305], [48.781918, 9.796500], [48.781073, 9.796162], [48.780476, 9.796229]],
    "options": { "strokeColor": "#E50000", "strokeThickness": 8 }
  }, {  ## rw_ab91029c (Auf den Hochwiesen) || east -> west
      "points": [[48.792796, 9.781156], [48.792906, 9.781330], [48.793076, 9.781738], [48.793362, 9.782492]],
      "options": { "strokeColor": "#E50000", "strokeThickness": 7 }
    }
]
## ------------------------------------------------------ Roadworks Polygons ---
## pg_roadworks = [
##   {
##       method: 'complex',
##       points: [ ## rw_04512462
##           [48.781832, 9.796397], [48.781796, 9.796504], ## north end
##           [48.781270, 9.796315], [48.781076, 9.796239], [48.780912, 9.796207], ## east side
##           [48.780735, 9.796251], [48.780743, 9.796115], ## south end
##           [48.781050, 9.796082], [48.781303, 9.796180] ## west end
##       ],
##       options: { fillColor: '#d66b6b90', strokeThickness: 0.5, strokeColor: '#b24242' }
##   },
##   {
##       method: 'complex',
##       points: [ ## rw_00c18301
##           [48.802665, 9.821715], [48.802743, 9.821700], ## west end
##           [48.803393, 9.830036], [48.803324, 9.830147]  ## east end
##       ],
##       options: { fillColor: '#d66b6b90', strokeThickness: 0.5, strokeColor: '#b24242' }
##   }
## ]
## ------------------------------------------------------- Energy Production ---
pp_energy = [
   {
      "location": [
         48.812412,
         9.805116
      ],
      "options": {
         "icon": "solarPark"
      },
      "metadata": {
         "id": "energy_01",
         "title": "Solarpark Mutlanger Heide",
         "description": "Solarpark - Stadtwerke Gmünd"
      }
   },
   {
      "location": [
         48.801872,
         9.875063
      ],
      "options": {
         "icon": "solarPark"
      },
      "metadata": {
         "id": "energy_02",
         "title": "Solarpark Gügling",
         "description": "Solarpark - Stadtwerke Gmünd"
      }
   },
   {
      "location": [
         48.77079,
         9.797041
      ],
      "options": {
         "icon": "pvStation"
      },
      "metadata": {
         "id": "energy_03",
         "title": "Fa. Dettinger",
         "description": "PV-Anlage - Stadtwerke Gmünd"
      }
   },
   {
      "location": [
         48.803116,
         9.799159
      ],
      "options": {
         "icon": "pvStation"
      },
      "metadata": {
         "id": "energy_04",
         "title": "E-Carport - Hofanlage",
         "description": "PV-Anlage - Stadtwerke Gmünd"
      }
   },
   {
      "location": [
         48.83191,
         9.821654
      ],
      "options": {
         "icon": "pvStation"
      },
      "metadata": {
         "id": "energy_05",
         "title": "Eichenrainschule – Erweiterungsbau",
         "description": "PV-Anlage - Stadtwerke Gmünd"
      }
   },
   {
      "location": [
         48.80508,
         9.803662
      ],
      "options": {
         "icon": "pvStation"
      },
      "metadata": {
         "id": "energy_06",
         "title": "Zentrallager Stadtwerke – Dachanlage & Sichtschutzwand",
         "description": "PV-Anlage - Stadtwerke Gmünd"
      }
   },
   {
      "location": [
         48.817177,
         9.753483
      ],
      "options": {
         "icon": "pvStation"
      },
      "metadata": {
         "id": "energy_07",
         "title": "Kindergarten Villa Holder",
         "description": "PV-Anlage - Stadtwerke Gmünd"
      }
   }
]
## ----------------------------------------------------- E-Charging stations ---
pp_echarging = [
  {
     "location": [48.8030774, 9.7991804 ],
     "options": {
        "icon": "chargingStation"
     },
     "metadata": {
        "id": "echarging_01",
        "title": "Charging Station",
        "access": "Customer Card from Stadtwerke Gmünd, RFID card",
        "address": "Bürgerstraße 5",
        "hours": "Mo.-Mi.: 8h-16.30h, Do.: 8h-18h, Fr.: 8h-12h",
        "operator": "Stadtwerke Schwäbisch Gmünd",
        "outlets": "2x Type 2 (32A, 3Ph), 1x Type 2 (16A, 3Ph), 3x EU Schuko (16A)"
     }
  }, {
     "location": [48.799452, 9.798487],
     "options": {
        "icon": "chargingStation"
     },
     "metadata": {
        "id": "echarging_02",
        "title": "Charging Station",
        "access": "RFID card, customer card available for transients inside the townhall",
        "address": "Marktplatz 1",
        "hours": "24/7",
        "operator": "Ladenetz",
        "outlets": "1x Type 2 (16A, 3Ph), 1x Type 2 (32A, 3Ph), 2x EU Schuko (16A)"
     }
  }, {
     "location": [48.798240, 9.789304],
     "options": {
        "icon": "chargingStation"
     },
     "metadata": {
        "id": "echarging_03",
        "title": "Charging Station",
        "access": "Inside the car dealership",
        "address": "Lorcher Straße 35",
        "hours": "Mo.-Fr.: 8h-18h, Sa.: 8h-13h",
        "operator": "Car dealership Wagenblast",
        "outlets": "2x Type 2 (16A, 1Ph)"
     }
  }, {
     "location": [48.8012583, 9.7900647],
     "options": {
        "icon": "chargingStation"
     },
     "metadata": {
        "id": "echarging_04",
        "title": "Charging Station",
        "access": "Customer Card from Stadtwerke Gmünd, RFID card",
        "address": "Bahnhofplatz 2",
        "hours": "24/7",
        "operator": "Stadtwerke Schwäbisch Gmünd",
        "outlets": "2x Type 2 (32A, 3Ph), 2x EU Schuko (16A)"
     }
  }, {
     "location": [48.7956521, 9.778758],
     "options": {
        "icon": "chargingStation"
     },
     "metadata": {
        "id": "echarging_05",
        "title": "Charging Station",
        "access": "Customer Card from Stadtwerke Gmünd, RFID card",
        "address": "Lorcher Straße 199",
        "hours": "24/7",
        "operator": "Stadtwerke Schwäbisch Gmünd",
        "outlets": "1x Type 2 (32A, 3Ph), 1x EU Schuko (16A)"
     }
  }, {
     "location": [48.7886253, 9.7630371],
     "options": {
        "icon": "chargingStation"
     },
     "metadata": {
        "id": "echarging_06",
        "title": "Charging Station",
        "access": "RFID card, no costs",
        "address": "Lorcher Straße 119",
        "hours": "24/7",
        "operator": "Stadtwerke Schwäbisch Gmünd",
        "outlets": "1x Type 2 (63A, 3Ph), 1x Combo CCS EU (50kW), 1x CHAdeMO DC (50kW)"
     }
  }, {
     "location": [48.7801488, 9.842118],
     "options": {
        "icon": "chargingStation"
     },
     "metadata": {
        "id": "echarging_07",
        "title": "Charging Station",
        "access": "Upon consultation: +49 7171 81988",
        "address": "In den Hagenäckern 58",
        "hours": "24/7",
        "operator": "BHKW-Ladepunkt",
        "outlets": "1x EU Schuko (16A), 1x CEE 400V (16A, 3Ph)"
     }
  }, {
     "location": [48.7959292, 9.8649182],
     "options": {
        "icon": "chargingStation"
     },
     "metadata": {
        "id": "echarging_08",
        "title": "Charging Station",
        "access": "Customer Card from Stadtwerke Gmünd, RFID card",
        "address": "Güglingstraße 66",
        "hours": "Mo.-Mi.: 8h-16.30h, Do.: 8h-18h, Fr.: 8h-12h",
        "operator": "Stadtwerke Schwäbisch Gmünd",
        "outlets": "2x Type 2 (32A, 3Ph)"
     }
  }, {
     "location": [48.7712213, 9.8306642],
     "options": {
        "icon": "chargingStation"
     },
     "metadata": {
        "id": "echarging_09",
        "title": "Charging Station",
        "access": "RWE customers or roaming partners",
        "address": "Waldstetten, Gottlieb-Daimler-Straße 20",
        "hours": "24/7",
        "operator": "RWE",
        "outlets": "2x Type 2 (32A, 3Ph)"
     }
  }, {
     "location": [48.798226, 9.789277],
     "options": {
        "icon": "chargingStation"
     },
     "metadata": {
        "id": "echarging_10",
        "title": "Charging Station",
        "access": "RFID card",
        "address": "Rektor-Klaus-Straße 9",
        "hours": "24/7",
        "operator": "EMIS",
        "outlets": "2x Type 2 (32A, 3Ph), 2x EU Schuko (32A, 3Ph)"
     }
  }, {
     "location": [48.800980, 9.785535],
     "options": {
        "icon": "chargingStation"
     },
     "metadata": {
        "id": "echarging_11",
        "title": "Charging Station",
        "access": "RFID card",
        "address": "Nepperbergstraße 7",
        "hours": "24/7",
        "operator": "Ladenetz",
        "outlets": "2x Type 2 (32A, 3Ph), 2x EU Schuko (32A, 1Ph)"
     }
  ## }, {
  ##    "location": [48.794948, 9.776921],
  ##    "options": {
  ##       "icon": "chargingStation"
  ##    },
  ##    "metadata": {
  ##       "id": "echarging_12",
  ##       "title": "Charging Station",
  ##       "access": "RFID card",
  ##       "address": "Lorcher Straße 119",
  ##       "hours": "24/7",
  ##       "operator": "EMIS",
  ##       "outlets": "1x Type 2 (32A, 3Ph), 1x EU Schuko (32A, 1Ph)"
  ##    }
  }, {
     "location": [48.813934, 9.772501],
     "options": {
        "icon": "chargingStation"
     },
     "metadata": {
        "id": "echarging_13",
        "title": "Charging Station",
        "access": "RFID card",
        "address": "Deinbacher Straße 45",
        "hours": "24/7",
        "operator": "Ladenetz",
        "outlets": "2x Type 2 (32A, 3Ph), 2x EU Schuko (32A, 1Ph)"
     }
  }, {
     "location": [48.792840, 9.822286],
     "options": {
        "icon": "chargingStation"
     },
     "metadata": {
        "id": "echarging_14",
        "title": "Charging Station",
        "access": "RFID card",
        "address": "Am Sonnenhügel 5",
        "hours": "24/7",
        "operator": "Stadtwerke Schwäbisch Gmünd",
        "outlets": "2x Type 2 (32A, 3Ph)"
     }
  }, {
     "location": [48.801033, 9.832993],
     "options": {
        "icon": "chargingStation"
     },
     "metadata": {
        "id": "echarging_15",
        "title": "Charging Station",
        "access": "RFID card",
        "address": "Buchstraße 200",
        "hours": "24/7",
        "operator": "Agip",
        "outlets": "1x Type 2 (63A, 3Ph), 1x Combo CSS EU (50kW), 1x CHAdeMO (50kW)"
     }
  }, {
     "location": [48.803989, 9.839488],
     "options": {
        "icon": "chargingStation"
     },
     "metadata": {
        "id": "echarging_15",
        "title": "Charging Station",
        "access": "RFID card",
        "address": "Hauptstraße 6",
        "hours": "24/7",
        "operator": "Ladenetz",
        "outlets": "1x Type 2 (32A, 3Ph), 1x Combo CSS EU (50kW), 1x CHAdeMO (50kW)"
     }
  }
]
## -------------------------------------------------------------- Congestion ---
pp_congestions = [
   {
      "location": [
         48.793976,
         9.779178
      ],
      "options": {
         "icon": "congestionSign"
      },
      "metadata": {
         "id": "congestions_01",
         "title": "Stuttgarter Straße",
         "description": "Congestion - Stuttgarter Straße"
      }
   },
   {
      "location": [
         48.808598,
         9.795713
      ],
      "options": {
         "icon": "congestionSign"
      },
      "metadata": {
         "id": "congestions_02",
         "title": "Mutlanger Straße",
         "description": "Congestion - Mutlanger Straße"
      }
   }
]
