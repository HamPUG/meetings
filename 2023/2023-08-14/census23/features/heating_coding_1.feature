Feature: Code Heating Classification

    Scenario: Code predfined input to classification
        Given a dwelling input table
            | dwell_nbr | d_heating_predefined                                  |
            | 1         | heat_pump,electric_heater                             |
            | 2         | fixed_gas_heater,portable_gas_heater,wood_burner      |
            | 3         | heat_pump,portable_gas_heater,pellet_fire,coal_burner |
            | 4         | electric_heater,other                                 |
            | 5         | heat_pump,dont_use                                    |
            | 6         | wood_burner,other,dont_use                            |
            | 7         | dont_use,wood_burner                                  |
            | 8         | dont_use,heat_pump,electric_heater                    |
        When the heating_coding_1 module is run
        Then the subset of output dwelling table is
            | d_heating_predefined_code | d_heating_code_data_source |
            | 01;02                     | 11                         |
            | 03;04;05                  | 11                         |
            | 01;04;06;07               | 11                         |
            | 02;08                     | 11                         |
            | 01;00                     | 11                         |
            | 05;08;00                  | 11                         |
            | 00;05                     | 11                         |
            | 00;01;02                  | 11                         |