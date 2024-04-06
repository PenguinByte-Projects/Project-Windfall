package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

type PackageInfo struct {
	Dependencies    []string `json:"dependencies"`
	InstallScript   string   `json:"install_script"`
	InstalledPath   string   `json:"installed_path"`
}

func installPackage(packageName string) {
	packageDir := filepath.Join("/packages", packageName)
	if _, err := os.Stat(packageDir); os.IsNotExist(err) {
		fmt.Printf("Package %s not found.\n", packageName)
		return
	}

	packageInfoBytes, err := ioutil.ReadFile(filepath.Join(packageDir, "package.json"))
	if err != nil {
		fmt.Println("Error reading package.json:", err)
		return
	}

	var packageInfo PackageInfo
	if err := json.Unmarshal(packageInfoBytes, &packageInfo); err != nil {
		fmt.Println("Error parsing package.json:", err)
		return
	}

	for _, dependency := range packageInfo.Dependencies {
		installPackage(dependency)
	}

	if packageInfo.InstallScript == "" {
		fmt.Printf("No install script specified for package %s.\n", packageName)
		return
	}

	// Assuming the install script is a shell script that can be executed directly
	// This is a simplification; in a real-world scenario, you might need to handle this differently
	scriptPath := filepath.Join(packageDir, packageInfo.InstallScript)
	cmd := exec.Command("sh", scriptPath, filepath.Join(packageDir, "package.json"), packageDir)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		fmt.Printf("Installation of %s failed: %v\n", packageName, err)
		return
	}

	if packageInfo.InstalledPath != "" {
		os.Setenv("PATH", os.Getenv("PATH")+string(os.PathListSeparator)+packageInfo.InstalledPath)
		fmt.Printf("Successfully added %s to PATH.\n", packageInfo.InstalledPath)
	} else {
		fmt.Println("Installation successful, but 'installed_path' is not specified in package.json.")
	}
}

func uninstallPackage(packageName string) {
	packageDir := filepath.Join("/packages", packageName)
	if _, err := os.Stat(packageDir); os.IsNotExist(err) {
		fmt.Printf("Package %s not found.\n", packageName)
		return
	}

	packageInfoBytes, err := ioutil.ReadFile(filepath.Join(packageDir, "package.json"))
	if err != nil {
		fmt.Println("Error reading package.json:", err)
		return
	}

	var packageInfo PackageInfo
	if err := json.Unmarshal(packageInfoBytes, &packageInfo); err != nil {
		fmt.Println("Error parsing package.json:", err)
		return
	}

	if packageInfo.InstalledPath != "" {
		newPath := strings.Replace(os.Getenv("PATH"), packageInfo.InstalledPath+string(os.PathListSeparator), "", 1)
		os.Setenv("PATH", newPath)
		fmt.Printf("Removed %s from PATH.\n", packageInfo.InstalledPath)

		if err := os.RemoveAll(packageInfo.InstalledPath); err != nil {
			fmt.Printf("Error removing %s: %v\n", packageInfo.InstalledPath, err)
		} else {
			fmt.Printf("Successfully uninstalled %s.\n", packageName)
		}
	} else {
		fmt.Println("Uninstallation successful, but 'installed_path' is not specified in package.json.")
	}
}

func main() {
	command := flag.String("command", "", "The command to execute: install or uninstall")
	packageName := flag.String("package_name", "", "The name of the package to manage")
	flag.Parse()

	if *command == "install" {
		installPackage(*packageName)
	} else if *command == "uninstall" {
		uninstallPackage(*packageName)
	} else {
		fmt.Println("Invalid command. Use 'install' or 'uninstall'.")
	}
}
