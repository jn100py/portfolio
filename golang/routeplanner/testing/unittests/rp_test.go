package unittests


import (

	"testing"
	"demo/application"
    "fmt"
    "strings"

)



// Location tests

func TestLocationInit(t *testing.T) {

    location := application.Location{Name: "Utrecht", X: 15, Y: 35}

	if location.X != 15 {
        t.Errorf("Initialization of Location with name Utrecht failed")
    }

}


func TestLocationCalculateDistance(t *testing.T) {

    locationUtrecht := application.Location{Name: "Utrecht", X: 15, Y: 35}
    locationZeist := application.Location{Name: "Zeist", X: 19, Y: 35}

    distance := locationUtrecht.CalculateDistance(locationZeist)

	if distance != 4 {
        t.Errorf("Wrong distance Utrecht-Zeist: %v", distance)
    }

}


func TestLocationAddConnection(t *testing.T) {

    locationUtrecht := application.Location{Name: "Utrecht", X: 15, Y: 35, Connections: make(map[string]int)}
    locationZeist := application.Location{Name: "Zeist", X: 19, Y: 35}

    locationUtrecht.AddConnection(locationZeist)

	if len(locationUtrecht.Connections) != 1 {
        t.Errorf("Wrong number of connections for Utrecht: %d", len(locationUtrecht.Connections))
    }

}



// Map tests

func TestMapInit(t *testing.T) {

	map1 := application.Map{Name: "Stuivezand"}

	if map1.Name != "Stuivezand" {
        t.Errorf("Wrong map name!")
    }

}


// Routeplanner tests

func TestRoutePlanner(t *testing.T) {

	map1 := application.Map{Name: "Stuivezand"}
	fpathDataMap1 := fmt.Sprintf("%s/data/map1.txt", application.GetProjectPath())
    fpathDataMap1 = strings.Replace(fpathDataMap1, "/testing/unittests", "", 1)

	_ = map1.ImportData(fpathDataMap1)

	rp := application.RoutePlanner{}
	rp.Loadmap(map1)
	_ = rp.SetStartEndLocation("Hertenpark", "Zwanenzang")
	rp.CalculateShortestPath()


	if rp.ShortestPathLength != 65 {
        t.Errorf("Wrong PathLength: %d!", rp.ShortestPathLength)
    }

}

