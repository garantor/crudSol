// SPDX-License-Identifier: MIT


pragma solidity >= 0.5.0;

contract CompanyStructCrud {
    // a sample crud smart contract
    /** 1. Create a country and add to a struct
    2. Read a country from a struct
    3. Update a country in the struct 
    4. Delete a Country from the struct 
    
    it should also have events that emit actions don on each of this countract which will be handle from web.py and send as a restful api
    */

    struct Countries {
        string name;
        string current_president;
        uint populations;
        uint list_0f_states;

    }

    mapping(string => Countries) Country;
    event countryDetails (
        string name,
        string current_president,
        uint populations,
        uint list_0f_states
    );

    constructor() public {
        Countries memory firstCountry = Countries("Nigeria", "Obasanjo", 420000000, 36);
        Country["Obasanjo"] = firstCountry;
    }


    function getCountryByPresident(string memory _president) external {
        Countries memory current_country = Country[_president];
        emit countryDetails(current_country.name, current_country.current_president, current_country.populations, current_country.list_0f_states);

    }

    function CreateCountry(string memory _name, string memory _president, uint  _populations, uint  _list_of_state) public {
        Country[_president] = Countries({name:_name, current_president:_president, populations:_populations, list_0f_states:_list_of_state});
        emit countryDetails(_name, _president, _populations, _list_of_state);

    }

    function UpdateCountry(string memory _president, uint _state) public {
        Countries memory countryToEdit = Country[_president];
        // updating state and pupolations
        countryToEdit.list_0f_states = _state;
        emit countryDetails(countryToEdit.name, countryToEdit.current_president, countryToEdit.populations, countryToEdit.list_0f_states);


    }


    function deleteCountry(string memory _president) public {
        delete Country[_president];

}

}