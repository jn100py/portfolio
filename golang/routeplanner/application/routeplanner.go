package application

import (
	"bufio"
	"demo/library/dijkstra"
	"fmt"
	"log"
	"math"
	"os"
	"path/filepath"
	"strings"
    "strconv"
)

func GetProjectPath() string {

	abs, err := filepath.Abs("./_")
	if err != nil {
		log.Fatalf("ERROR Unknown filepath:", abs)
	}

	projectPath := filepath.Dir(abs)
	return projectPath

}

func readFile(filepath string) []string {

	file, err := os.Open(filepath)

	if err != nil {
		log.Fatalf("ERROR Failed to open file: %s", err)
	}

	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	var txtLines []string

	for scanner.Scan() {
		txtLines = append(txtLines, scanner.Text())
	}

	file.Close()

    return txtLines

}

func findLocationInLocationList(name string, x int, y int, locationList []Location) []Location {

	var hits []Location

	for i := 0; i < len(locationList); i++ {

		if loc := locationList[i]; (loc.Name == name || name == "-1") && (loc.X == x || x == -1) && (loc.Y == y || y == -1) {

			hits = append(hits, loc)

		}

	}

	return hits

}


type Location struct {
	Name        string
	X           int
	Y           int
	Connections map[string]int
}

func (l *Location) ShowState() {
	fmt.Printf("Location       : %s\n" +
               "x, y           : %d %d\n" +
               "connected with : %v\n\n", l.Name, l.X, l.Y, l.Connections)
}

func (l *Location) CalculateDistance(l2 Location) int {

	deltaX := float64(l.X - l2.X)
	deltaY := float64(l.Y - l2.Y)
	distance := int(math.Sqrt(math.Pow(deltaX, 2) + math.Pow(deltaY, 2)))

	return distance

}

func (l *Location) AddConnection(l2 Location) {

	l.Connections[l2.Name] = l.CalculateDistance(l2)

}



type Map struct {
	Name      string
	locations []Location
}

func (m *Map) ShowState() {

	fmt.Printf("%s -> Number of Locations : %d\n\n", m.Name, len(m.locations))
    fmt.Printf("Locations:\n")
	for i := 0; i < len(m.locations); i++ {

		locationName := m.locations[i].Name
		connections := m.locations[i].Connections
		fmt.Printf("    %s\n    / Connections: %v\n\n", locationName, connections)

	}

}

func (m *Map) addLocation(location Location) {

    m.locations = append(m.locations, location)

}

func (m *Map) find(locationName string, x int, y int) []Location {

    hits := findLocationInLocationList(locationName, x, y, m.locations)

	return hits

}

func (m *Map) ImportData(filepath string) bool {

    var dataLines = readFile(filepath)

    // First we proces the locations (the first column in the data)

	for _, line := range dataLines {

		lineValues := strings.Split(line, ",")

        locationName := lineValues[0]
        xValue, _ := strconv.Atoi(lineValues[1])
        yValue, _ := strconv.Atoi(lineValues[2])

		location := Location{Name: locationName, X: xValue, Y: yValue, Connections: make(map[string]int)}
        m.addLocation(location)

	}

    // Finally, we proces the connections

	for _, line := range dataLines {

		lineValues := strings.Split(line, ",")

		locationName := lineValues[0]
		hits := m.find(locationName, -1, -1)
        if len(hits) == 0 {
            fmt.Printf("ERROR Unknown location name: %s\n", locationName)
            return false
        }
		location := hits[0]

		for _, connectionName := range lineValues[3:] {

			hits := m.find(connectionName, -1, -1)
            if len(hits) == 0 {
                fmt.Printf("ERROR Unknown connection name: %s\n", connectionName)
                return false
            }

			locationConnection := hits[0]
			location.AddConnection(locationConnection)
		}
	}

    return true

}

func (m *Map) Display() {

    var printLocation = func(x int, y int, locationName string) {

		extraNrSpaces := 0
		if y < 10 {
			extraNrSpaces = 1
		}
		spaces := strings.Repeat(" ", x + extraNrSpaces)
		fmt.Printf("%s X %s", spaces, locationName)

    }

    fmt.Printf("\n\n\n    - %s -\n", m.Name)
	for y := 100; y >= 0; y = y - 5 {
		locationsThisRow := m.find("-1", -1, y)

		fmt.Printf("%d", y)

		if len(locationsThisRow) > 0 {

			for x := 0; x <= 100; x = x + 5 {
				locationsThisRowAndColumn := findLocationInLocationList("-1", x, y, locationsThisRow)

				if len(locationsThisRowAndColumn) > 0 {

                    printLocation(x, y, locationsThisRowAndColumn[0].Name)

				}
			}
			fmt.Printf("\n")

		} else {

			fmt.Printf("\n")

		}
	}
}


type RoutePlanner struct {
	activeMap     Map

	startLocation Location
	endLocation   Location

    ShortestPath []string
    ShortestPathLength int

}

func (rp *RoutePlanner) ShowState() {

	fmt.Printf("Map %s is currently active and has %d locations\n", 
                    rp.activeMap.Name, 
                    len(rp.activeMap.locations))
	fmt.Printf("Start location is : %s\n", rp.startLocation.Name)
	fmt.Printf("  End location is : %s\n", rp.endLocation.Name)

    fmt.Printf("\n\nShortest Path is %s with length %d\n", rp.ShortestPath, rp.ShortestPathLength)

}

func (rp *RoutePlanner) Loadmap(m Map) {

	rp.activeMap = m

}

func (rp *RoutePlanner) SetStartEndLocation(startlocationName string, endlocationName string) bool {

	hits := rp.activeMap.find(startlocationName, -1, -1)
    if len(hits) == 0 {
        return false
    }
    rp.startLocation = hits[0]


	hits = rp.activeMap.find(endlocationName, -1, -1)
    if len(hits) == 0 {
        return false
    }
	rp.endLocation = hits[0]

    return true
}

func (rp *RoutePlanner) CalculateShortestPath() {

	graph := dijkstra.Graph{}

	for i := 0; i < len(rp.activeMap.locations); i++ {

		location := rp.activeMap.locations[i]
		graph[location.Name] = location.Connections

	}

	rp.ShortestPath, rp.ShortestPathLength, _ = graph.Path(rp.startLocation.Name, rp.endLocation.Name)

}


