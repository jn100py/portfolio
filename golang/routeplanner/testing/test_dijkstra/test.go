package main

import (
	"demo/library/dijkstra"
	"fmt"
)

// cd <path/2/>/test_dijkstra
// go run test.go

func main() {

	// based on an example in https://www.freecodecamp.org/news/dijkstras-shortest-path-algorithm-visual-introduction/

	/*	g := dijkstra.Graph{
		"0": {"1": 2, "2": 6},
		"1": {"3": 5},
		"2": {"0": 6, "3": 8},
		"3": {"1": 5, "2": 8, "4": 10, "5": 15},
		"4": {"3": 10, "5": 6, "6": 2},
		"5": {"3": 15, "4": 6, "6": 6},
		"6": {"4": 2, "5": 6},
	}*/

	g := dijkstra.Graph{}
	m := make(map[string]int)
	m["1"] = 2
	m["2"] = 6
	g["0"] = m

	m = make(map[string]int)
	m["3"] = 5
	g["1"] = m

	m = make(map[string]int)
	m["0"] = 6
	m["3"] = 8
	g["2"] = m

	m = make(map[string]int)
	m["1"] = 5
	m["2"] = 8
	m["4"] = 10
	m["5"] = 15
	g["3"] = m

	m = make(map[string]int)
	m["3"] = 10
	m["5"] = 6
	m["6"] = 2
	g["4"] = m

	m = make(map[string]int)
	m["3"] = 15
	m["4"] = 6
	m["6"] = 6
	g["5"] = m

	m = make(map[string]int)
	m["4"] = 2
	m["5"] = 6
	g["6"] = m

	path, cost, _ := g.Path("0", "6")
	fmt.Printf("Shortest Path is %s with length %d\n", path, cost)

}
