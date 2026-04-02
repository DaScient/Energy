use std::f64::consts::PI;

struct Coordinate {
    channel_id: u32,
    x: f64,
    y: f64,
    z: f64,
}

/// Generates a volumetric 3D map of electrode coordinates for a spherical mesh.
/// This allows the digital layer to map physical tissue space to array channels.
fn generate_fibonacci_sphere(num_channels: u32, radius_um: f64) -> Vec<Coordinate> {
    let mut map: Vec<Coordinate> = Vec::with_capacity(num_channels as usize);
    let phi = PI * (3.0 - (5.0_f64).sqrt()); // Golden angle

    for i in 0..num_channels {
        let y = 1.0 - (i as f64 / (num_channels as f64 - 1.0)) * 2.0; // y goes from 1 to -1
        let radius_at_y = (1.0 - y * y).sqrt();
        let theta = phi * (i as f64);

        let x = f64::cos(theta) * radius_at_y;
        let z = f64::sin(theta) * radius_at_y;

        map.push(Coordinate {
            channel_id: i,
            x: x * radius_um,
            y: y * radius_um,
            z: z * radius_um,
        });
    }
    map
}

fn main() {
    let tissue_radius = 1500.0; // 1.5mm
    let electrode_map = generate_fibonacci_sphere(1024, tissue_radius);
    println!("Generated 3D volumetric map for {} channels.", electrode_map.len());
    // Export logic to JSON/CSV for the signal processing pipeline
}
