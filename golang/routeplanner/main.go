package main

import (
	"fmt"
	"os"
	"demo/application"
)


func main() {

	map1 := application.Map{Name: "Stuivezand"}
	fpathDataMap1 := fmt.Sprintf("%s/data/map1.txt", application.GetProjectPath())

	var success = map1.ImportData(fpathDataMap1)
    if success == false {
    	fmt.Printf("INFO Import failed\n")
        os.Exit(1)
    }

	fmt.Printf("\n\n")
	map1.ShowState()
	map1.Display()


	rp := application.RoutePlanner{}
	rp.Loadmap(map1)

	success = rp.SetStartEndLocation("Everveen", "Hertenpark")
    if success == false {
    	fmt.Printf("ERROR Unknown start or end location\n")
        os.Exit(1)
    }

	rp.CalculateShortestPath()
	fmt.Printf("\n\n")
    rp.ShowState()

}

