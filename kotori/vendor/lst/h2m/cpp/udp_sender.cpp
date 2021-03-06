// -*- coding: utf-8 -*-
// (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
#include <stdio.h>
#include <iostream>
#include <string>

#include <h2m_structs.h>
#include <udp.h>
#include <util.h>

#define header(label, thing) \
    std::cout << "---" << "\n" << \
    "name:   " << label << "\n" \
    "id:     " << std::to_string(thing.ID) << "\n" << \
    "length: " << std::to_string(thing.length) << "\n"
#define message(thing) hexlify(&thing, sizeof(thing) - 1);
#define dump(label, thing) header(label, thing); message(thing)
#define dump_and_send(label, thing) dump(label, thing); client.send(&thing, sizeof(thing))

int main() {

    //std::cout << "Hello World!" << "\n";

    udp_client_server::udp_client client("localhost", 8888);

    // 0. program
    static struct_program program;
    //bzero(&program, sizeof(program));
    program.send_ser = 1;
    program.cfg_loaded = 1;
    program.gps_data = 65;
    program.ser_sync = 1;
    dump_and_send("program", program);

    // 1. request
    static struct_request request;
    request.akt = 1;
    request.internet_s = 1;
    dump_and_send("request", request);

    // 2. struct_cap_r
    static struct_cap_r cap_r;
    cap_r.voltage_act = 40;
    dump_and_send("cap_r", cap_r);

    // 3. struct_cap_w
    static struct_cap_w cap_w;
    cap_w.voltage_low = 10;
    dump_and_send("cap_w", cap_w);

    // 4. struct_fuelcell_r
    static struct_fuelcell_r fuelcell_r;
    fuelcell_r.current_act = 3;
    dump_and_send("fuelcell_r", fuelcell_r);

    // 5. struct_fuelcell_w
    static struct_fuelcell_w fuelcell_w;
    fuelcell_w.temp_max = 80;
    fuelcell_w.voltage_max = 120;
    dump_and_send("fuelcell_w", fuelcell_w);

    // 19. struct_gps_w
    static struct_gps_w gps_w;
    gps_w.position_x = 99;
    gps_w.position_y = 101;
    dump_and_send("gps_w", gps_w);

    return 0;
}
