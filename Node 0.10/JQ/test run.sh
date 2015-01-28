#!/bin/bash

function test_jq {
    
    # Return the first object in the array
    echo "First object in the array"
    echo "-------------------------"
    eval "http $1 -b | jq '.[0]'"
    
    # Get the id and name from each object
    echo "Name and ID from each object in the array"
    echo "-----------------------------------------"
    eval "http $1 -b | jq '[.[] | [.id, .name]]'"
}

test_jq 'https://gist.githubusercontent.com/jacobbridges/d1ef5a3cb68266589634/raw/e52262286efcb14b43d88017e8fba81a5eb78e6b/data.json'
