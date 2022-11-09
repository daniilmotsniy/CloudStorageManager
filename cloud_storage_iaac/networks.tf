resource "google_compute_network" "vpc_network" {
  name                    = "cloud-storage-manager-network"
  auto_create_subnetworks = false
  mtu                     = 1460
}

resource "google_compute_subnetwork" "default" {
  name          = "cloud-storage-manager-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = "europe-central2"
  network       = google_compute_network.vpc_network.id
}

resource "google_compute_firewall" "ssh" {
  name = "allow-ssh"
  allow {
    ports    = ["22"]
    protocol = "tcp"
  }
  direction     = "INGRESS"
  network       = google_compute_network.vpc_network.id
  priority      = 1000
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ssh"]
}

resource "google_compute_firewall" "cloud-storage-manager" {
  name    = "cloud-storage-manager-firewall"
  network = google_compute_network.vpc_network.id

  allow {
    protocol = "tcp"
    ports    = ["8000"]
  }
  source_ranges = ["0.0.0.0/0"]
}
