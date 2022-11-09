resource "google_compute_instance" "default" {
  name         = "cloud-storage-manager-vm"
  machine_type = "f1-micro"
  zone         = "europe-central2-a"
  tags         = ["ssh"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  # Install Python and Git
  metadata_startup_script = "sudo apt-get update; sudo apt-get install git; sudo apt-get install -yq build-essential python3-pip rsync"

  network_interface {
    subnetwork = google_compute_subnetwork.default.id

    access_config {
      # Include this section to give the VM an external IP address
    }
  }
}