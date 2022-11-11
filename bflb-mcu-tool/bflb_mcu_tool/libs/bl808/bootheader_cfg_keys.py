# -*- coding:utf-8 -*-


clock_start_pos = 100 # 0x64
bootcfg_start_pos = 128 # 0x80
bootcfg_len = 48
bootcpucfg_start_pos = bootcfg_start_pos+bootcfg_len # 176 0xB0
bootcpucfg_len = 24
bootcpucfg_m0_index = 0
bootcpucfg_d0_index = 1
bootcpucfg_lp_index = 2

boot2_start_pos = bootcpucfg_start_pos+bootcpucfg_len * (bootcpucfg_lp_index + 1) # 248 0xF8
boot2_len = 8

flashcfg_table_start_pos = boot2_start_pos+boot2_len # 256 0x100
flashcfg_table_len = 8

patch_on_read_start_pos = flashcfg_table_start_pos+flashcfg_table_len # 264 0x108
patch_on_read_len = 32

patch_on_jump_start_pos = patch_on_read_start_pos+patch_on_read_len # 296 0x128
patch_on_jump_len = 32

rsvd_start_pos = patch_on_jump_start_pos+patch_on_jump_len # 328 0x148
rsvd_len = 20

crc32_start_pos = rsvd_start_pos+rsvd_len # 348 0x15C

bootheader_len = crc32_start_pos+4 # 352 0x160

bootheader_cfg_keys = {
    "magic_code": {
        "offset": "0",
        "pos": "0",
        "bitlen": "32"
    },
    "revision": {
        "offset": "4",
        "pos": "0",
        "bitlen": "32"
    },
    # flash cfg
    "flashcfg_magic_code": {
        "offset": "8",
        "pos": "0",
        "bitlen": "32"
    },
    "io_mode": {
        "offset": "12",
        "pos": "0",
        "bitlen": "8"
    },
    "cont_read_support": {
        "offset": "12",
        "pos": "8",
        "bitlen": "8"
    },
    "sfctrl_clk_delay": {
        "offset": "12",
        "pos": "16",
        "bitlen": "8"
    },
    "sfctrl_clk_invert": {
        "offset": "12",
        "pos": "24",
        "bitlen": "8"
    },
    "reset_en_cmd": {
        "offset": "16",
        "pos": "0",
        "bitlen": "8"
    },
    "reset_cmd": {
        "offset": "16",
        "pos": "8",
        "bitlen": "8"
    },
    "exit_contread_cmd": {
        "offset": "16",
        "pos": "16",
        "bitlen": "8"
    },
    "exit_contread_cmd_size": {
        "offset": "16",
        "pos": "24",
        "bitlen": "8"
    },
    "jedecid_cmd": {
        "offset": "20",
        "pos": "0",
        "bitlen": "8"
    },
    "jedecid_cmd_dmy_clk": {
        "offset": "20",
        "pos": "8",
        "bitlen": "8"
    },
    "enter_32bits_addr_cmd": {
        "offset": "20",
        "pos": "16",
        "bitlen": "8"
    },
    "exit_32bits_addr_clk": {
        "offset": "20",
        "pos": "24",
        "bitlen": "8"
    },
    "sector_size": {
        "offset": "24",
        "pos": "0",
        "bitlen": "8"
    },
    "mfg_id": {
        "offset": "24",
        "pos": "8",
        "bitlen": "8"
    },
    "page_size": {
        "offset": "24",
        "pos": "16",
        "bitlen": "16"
    },
    "chip_erase_cmd": {
        "offset": "28",
        "pos": "0",
        "bitlen": "8"
    },
    "sector_erase_cmd": {
        "offset": "28",
        "pos": "8",
        "bitlen": "8"
    },
    "blk32k_erase_cmd": {
        "offset": "28",
        "pos": "16",
        "bitlen": "8"
    },
    "blk64k_erase_cmd": {
        "offset": "28",
        "pos": "24",
        "bitlen": "8"
    },
    "write_enable_cmd": {
        "offset": "32",
        "pos": "0",
        "bitlen": "8"
    },
    "page_prog_cmd": {
        "offset": "32",
        "pos": "8",
        "bitlen": "8"
    },
    "qpage_prog_cmd": {
        "offset": "32",
        "pos": "16",
        "bitlen": "8"
    },
    "qual_page_prog_addr_mode": {
        "offset": "32",
        "pos": "24",
        "bitlen": "8"
    },
    "fast_read_cmd": {
        "offset": "36",
        "pos": "0",
        "bitlen": "8"
    },
    "fast_read_dmy_clk": {
        "offset": "36",
        "pos": "8",
        "bitlen": "8"
    },
    "qpi_fast_read_cmd": {
        "offset": "36",
        "pos": "16",
        "bitlen": "8"
    },
    "qpi_fast_read_dmy_clk": {
        "offset": "36",
        "pos": "24",
        "bitlen": "8"
    },
    "fast_read_do_cmd": {
        "offset": "40",
        "pos": "0",
        "bitlen": "8"
    },
    "fast_read_do_dmy_clk": {
        "offset": "40",
        "pos": "8",
        "bitlen": "8"
    },
    "fast_read_dio_cmd": {
        "offset": "40",
        "pos": "16",
        "bitlen": "8"
    },
    "fast_read_dio_dmy_clk": {
        "offset": "40",
        "pos": "24",
        "bitlen": "8"
    },
    "fast_read_qo_cmd": {
        "offset": "44",
        "pos": "0",
        "bitlen": "8"
    },
    "fast_read_qo_dmy_clk": {
        "offset": "44",
        "pos": "8",
        "bitlen": "8"
    },
    "fast_read_qio_cmd": {
        "offset": "44",
        "pos": "16",
        "bitlen": "8"
    },
    "fast_read_qio_dmy_clk": {
        "offset": "44",
        "pos": "24",
        "bitlen": "8"
    },
    "qpi_fast_read_qio_cmd": {
        "offset": "48",
        "pos": "0",
        "bitlen": "8"
    },
    "qpi_fast_read_qio_dmy_clk": {
        "offset": "48",
        "pos": "8",
        "bitlen": "8"
    },
    "qpi_page_prog_cmd": {
        "offset": "48",
        "pos": "16",
        "bitlen": "8"
    },
    "write_vreg_enable_cmd": {
        "offset": "48",
        "pos": "24",
        "bitlen": "8"
    },
    "wel_reg_index": {
        "offset": "52",
        "pos": "0",
        "bitlen": "8"
    },
    "qe_reg_index": {
        "offset": "52",
        "pos": "8",
        "bitlen": "8"
    },
    "busy_reg_index": {
        "offset": "52",
        "pos": "16",
        "bitlen": "8"
    },
    "wel_bit_pos": {
        "offset": "52",
        "pos": "24",
        "bitlen": "8"
    },
    "qe_bit_pos": {
        "offset": "56",
        "pos": "0",
        "bitlen": "8"
    },
    "busy_bit_pos": {
        "offset": "56",
        "pos": "8",
        "bitlen": "8"
    },
    "wel_reg_write_len": {
        "offset": "56",
        "pos": "16",
        "bitlen": "8"
    },
    "wel_reg_read_len": {
        "offset": "56",
        "pos": "24",
        "bitlen": "8"
    },
    "qe_reg_write_len": {
        "offset": "60",
        "pos": "0",
        "bitlen": "8"
    },
    "qe_reg_read_len": {
        "offset": "60",
        "pos": "8",
        "bitlen": "8"
    },
    "release_power_down": {
        "offset": "60",
        "pos": "16",
        "bitlen": "8"
    },
    "busy_reg_read_len": {
        "offset": "60",
        "pos": "24",
        "bitlen": "8"
    },
    "reg_read_cmd0": {
        "offset": "64",
        "pos": "0",
        "bitlen": "8"
    },
    "reg_read_cmd1": {
        "offset": "64",
        "pos": "8",
        "bitlen": "8"
    },
    "reg_write_cmd0": {
        "offset": "68",
        "pos": "0",
        "bitlen": "8"
    },
    "reg_write_cmd1": {
        "offset": "68",
        "pos": "8",
        "bitlen": "8"
    },
    "enter_qpi_cmd": {
        "offset": "72",
        "pos": "0",
        "bitlen": "8"
    },
    "exit_qpi_cmd": {
        "offset": "72",
        "pos": "8",
        "bitlen": "8"
    },
    "cont_read_code": {
        "offset": "72",
        "pos": "16",
        "bitlen": "8"
    },
    "cont_read_exit_code": {
        "offset": "72",
        "pos": "24",
        "bitlen": "8"
    },
    "burst_wrap_cmd": {
        "offset": "76",
        "pos": "0",
        "bitlen": "8"
    },
    "burst_wrap_dmy_clk": {
        "offset": "76",
        "pos": "8",
        "bitlen": "8"
    },
    "burst_wrap_data_mode": {
        "offset": "76",
        "pos": "16",
        "bitlen": "8"
    },
    "burst_wrap_code": {
        "offset": "76",
        "pos": "24",
        "bitlen": "8"
    },
    "de_burst_wrap_cmd": {
        "offset": "80",
        "pos": "0",
        "bitlen": "8"
    },
    "de_burst_wrap_cmd_dmy_clk": {
        "offset": "80",
        "pos": "8",
        "bitlen": "8"
    },
    "de_burst_wrap_code_mode": {
        "offset": "80",
        "pos": "16",
        "bitlen": "8"
    },
    "de_burst_wrap_code": {
        "offset": "80",
        "pos": "24",
        "bitlen": "8"
    },
    "sector_erase_time": {
        "offset": "84",
        "pos": "0",
        "bitlen": "16"
    },
    "blk32k_erase_time": {
        "offset": "84",
        "pos": "16",
        "bitlen": "16"
    },
    "blk64k_erase_time": {
        "offset": "88",
        "pos": "0",
        "bitlen": "16"
    },
    "page_prog_time": {
        "offset": "88",
        "pos": "16",
        "bitlen": "16"
    },
    "chip_erase_time": {
        "offset": "92",
        "pos": "0",
        "bitlen": "16"
    },
    "power_down_delay": {
        "offset": "92",
        "pos": "16",
        "bitlen": "8"
    },
    "qe_data": {
        "offset": "92",
        "pos": "24",
        "bitlen": "8"
    },
    "flashcfg_crc32": {
        "offset": "96",
        "pos": "0",
        "bitlen": "32"
    },
    # clk cfg
    # clock start=100
    "clkcfg_magic_code": {
        "offset": str(int(clock_start_pos)+0),
        "pos": "0",
        "bitlen": "32"
    },
    "xtal_type": {
        "offset": str(int(clock_start_pos)+4),
        "pos": "0",
        "bitlen": "8"
    },
    "mcu_clk": {
        "offset": str(int(clock_start_pos)+4),
        "pos": "8",
        "bitlen": "8"
    },
    "mcu_clk_div": {
        "offset": str(int(clock_start_pos)+4),
        "pos": "16",
        "bitlen": "8"
    },
    "mcu_bclk_div": {
        "offset": str(int(clock_start_pos)+4),
        "pos": "24",
        "bitlen": "8"
    },
    "mcu_pbclk_div": {
        "offset": str(int(clock_start_pos)+8),
        "pos": "0",
        "bitlen": "8"
    },
    "lp_div": {
        "offset": str(int(clock_start_pos)+8),
        "pos": "8",
        "bitlen": "8"
    },
    "dsp_clk": {
        "offset": str(int(clock_start_pos)+8),
        "pos": "16",
        "bitlen": "8"
    },
    "dsp_clk_div": {
        "offset": str(int(clock_start_pos)+8),
        "pos": "24",
        "bitlen": "8"
    },
    "dsp_bclk_div": {
        "offset": str(int(clock_start_pos)+12),
        "pos": "0",
        "bitlen": "8"
    },
    "dsp_pbclk": {
        "offset": str(int(clock_start_pos)+12),
        "pos": "8",
        "bitlen": "8"
    },
    "dsp_pbclk_div": {
        "offset": str(int(clock_start_pos)+12),
        "pos": "16",
        "bitlen": "8"
    },
    "emi_clk": {
        "offset": str(int(clock_start_pos)+12),
        "pos": "24",
        "bitlen": "8"
    },
    "emi_clk_div": {
        "offset": str(int(clock_start_pos)+16),
        "pos": "0",
        "bitlen": "8"
    },
    "flash_clk_type": {
        "offset": str(int(clock_start_pos)+16),
        "pos": "8",
        "bitlen": "8"
    },
    "flash_clk_div": {
        "offset": str(int(clock_start_pos)+16),
        "pos": "16",
        "bitlen": "8"
    },
    "wifipll_pu": {
        "offset": str(int(clock_start_pos)+16),
        "pos": "24",
        "bitlen": "8"
    },
    "aupll_pu": {
        "offset": str(int(clock_start_pos)+20),
        "pos": "0",
        "bitlen": "8"
    },
    "cpupll_pu": {
        "offset": str(int(clock_start_pos)+20),
        "pos": "8",
        "bitlen": "8"
    },
    "mipipll_pu": {
        "offset": str(int(clock_start_pos)+20),
        "pos": "16",
        "bitlen": "8"
    },
    "uhspll_pu": {
        "offset": str(int(clock_start_pos)+20),
        "pos": "24",
        "bitlen": "8"
    },
    "clkcfg_crc32": {
        "offset": str(int(clock_start_pos)+24),
        "pos": "0",
        "bitlen": "32"
    },
    # bootcfg
    "sign": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "0",
        "bitlen": "2"
    },
    "encrypt_type": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "2",
        "bitlen": "2"
    },
    "key_sel": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "4",
        "bitlen": "2"
    },
    "xts_mode": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "6",
        "bitlen": "1"
    },
    "aes_region_lock": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "7",
        "bitlen": "1"
    },
    "no_segment": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "8",
        "bitlen": "1"
    },
    "boot2_enable": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "9",
        "bitlen": "1"
    },
    "boot2_rollback": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "10",
        "bitlen": "1"
    },
    "cpu_master_id": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "11",
        "bitlen": "4"
    },
    "notload_in_bootrom": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "15",
        "bitlen": "1"
    },
    "crc_ignore": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "16",
        "bitlen": "1"
    },
    "hash_ignore": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "17",
        "bitlen": "1"
    },
    "power_on_mm": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "18",
        "bitlen": "1"
    },
    "em_sel": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "19",
        "bitlen": "3"
    },
    "cmds_en": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "22",
        "bitlen": "1"
    },
    "cmds_wrap_mode": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "23",
        "bitlen": "2"
    },
    "cmds_wrap_len": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "25",
        "bitlen": "4"
    },
    "icache_invalid": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "29",
        "bitlen": "1"
    },
    "dcache_invalid": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "30",
        "bitlen": "1"
    },
    "fpga_halt_release": {
        "offset": str(int(bootcfg_start_pos)+0),
        "pos": "31",
        "bitlen": "1"
    },
    # flash controller offset
    "group_image_offset": {
        "offset": str(int(bootcfg_start_pos)+4),
        "pos": "0",
        "bitlen": "32"
    },
    "aes_region_len": {
        "offset": str(int(bootcfg_start_pos)+8),
        "pos": "0",
        "bitlen": "32"
    },
    # total image len or segment count
    "img_len_cnt": {
        "offset": str(int(bootcfg_start_pos)+12),
        "pos": "0",
        "bitlen": "32"
    },
    # img hash
    "hash_0": {
        "offset": str(int(bootcfg_start_pos)+16),
        "pos": "0",
        "bitlen": "32"
    },
    "hash_1": {
        "offset": str(int(bootcfg_start_pos)+20),
        "pos": "0",
        "bitlen": "32"
    },
    "hash_2": {
        "offset": str(int(bootcfg_start_pos)+24),
        "pos": "0",
        "bitlen": "32"
    },
    "hash_3": {
        "offset": str(int(bootcfg_start_pos)+28),
        "pos": "0",
        "bitlen": "32"
    },
    "hash_4": {
        "offset": str(int(bootcfg_start_pos)+32),
        "pos": "0",
        "bitlen": "32"
    },
    "hash_5": {
        "offset": str(int(bootcfg_start_pos)+36),
        "pos": "0",
        "bitlen": "32"
    },
    "hash_6": {
        "offset": str(int(bootcfg_start_pos)+40),
        "pos": "0",
        "bitlen": "32"
    },
    "hash_7": {
        "offset": str(int(bootcfg_start_pos)+44),
        "pos": "0",
        "bitlen": "32"
    },
    # boot cpu m0 config
    "m0_config_enable": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_m0_index)+0),
        "pos": "0",
        "bitlen": "8"
    },
    "m0_halt_cpu": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_m0_index)+0),
        "pos": "8",
        "bitlen": "8"
    },
    "m0_cache_enable": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_m0_index)+0),
        "pos": "16",
        "bitlen": "1"
    },
    "m0_cache_wa": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_m0_index)+0),
        "pos": "17",
        "bitlen": "1"
    },
    "m0_cache_wb": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_m0_index)+0),
        "pos": "18",
        "bitlen": "1"
    },
    "m0_cache_wt": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_m0_index)+0),
        "pos": "19",
        "bitlen": "1"
    },
    "m0_cache_way_dis": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_m0_index)+0),
        "pos": "20",
        "bitlen": "4"
    },
    "m0_reserved": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_m0_index)+0),
        "pos": "24",
        "bitlen": "8"
    },
    "m0_cache_range_h": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_m0_index)+4),
        "pos": "0",
        "bitlen": "32"
    },
    "m0_cache_range_l": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_m0_index)+8),
        "pos": "0",
        "bitlen": "32"
    },
    "m0_image_address_offset": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_m0_index)+12),
        "pos": "0",
        "bitlen": "32"
    },
    "m0_boot_entry": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_m0_index)+16),
        "pos": "0",
        "bitlen": "32"
    },
    "m0_msp_val": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_m0_index)+20),
        "pos": "0",
        "bitlen": "32"
    },
    # boot cpu d0 config
    "d0_config_enable": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_d0_index)+0),
        "pos": "0",
        "bitlen": "8"
    },
    "d0_halt_cpu": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_d0_index)+0),
        "pos": "8",
        "bitlen": "8"
    },
    "d0_cache_enable": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_d0_index)+0),
        "pos": "16",
        "bitlen": "1"
    },
    "d0_cache_wa": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_d0_index)+0),
        "pos": "17",
        "bitlen": "1"
    },
    "d0_cache_wb": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_d0_index)+0),
        "pos": "18",
        "bitlen": "1"
    },
    "d0_cache_wt": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_d0_index)+0),
        "pos": "19",
        "bitlen": "1"
    },
    "d0_cache_way_dis": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_d0_index)+0),
        "pos": "20",
        "bitlen": "4"
    },
    "d0_reserved": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_d0_index)+0),
        "pos": "24",
        "bitlen": "8"
    },
    "d0_cache_range_h": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_d0_index)+4),
        "pos": "0",
        "bitlen": "32"
    },
    "d0_cache_range_l": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_d0_index)+8),
        "pos": "0",
        "bitlen": "32"
    },
    "d0_image_address_offset": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_d0_index)+12),
        "pos": "0",
        "bitlen": "32"
    },
    "d0_boot_entry": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_d0_index)+16),
        "pos": "0",
        "bitlen": "32"
    },
    "d0_msp_val": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_d0_index)+20),
        "pos": "0",
        "bitlen": "32"
    },
    # boot cpu lp config
    "lp_config_enable": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_lp_index)+0),
        "pos": "0",
        "bitlen": "8"
    },
    "lp_halt_cpu": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_lp_index)+0),
        "pos": "8",
        "bitlen": "8"
    },
    "lp_cache_enable": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_lp_index)+0),
        "pos": "16",
        "bitlen": "1"
    },
    "lp_cache_wa": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_lp_index)+0),
        "pos": "17",
        "bitlen": "1"
    },
    "lp_cache_wb": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_lp_index)+0),
        "pos": "18",
        "bitlen": "1"
    },
    "lp_cache_wt": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_lp_index)+0),
        "pos": "19",
        "bitlen": "1"
    },
    "lp_cache_way_dis": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_lp_index)+0),
        "pos": "20",
        "bitlen": "4"
    },
    "lp_reserved": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_lp_index)+0),
        "pos": "24",
        "bitlen": "8"
    },
    "lp_cache_range_h": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_lp_index)+4),
        "pos": "0",
        "bitlen": "32"
    },
    "lp_cache_range_l": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_lp_index)+8),
        "pos": "0",
        "bitlen": "32"
    },
    "lp_image_address_offset": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_lp_index)+12),
        "pos": "0",
        "bitlen": "32"
    },
    "lp_boot_entry": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_lp_index)+16),
        "pos": "0",
        "bitlen": "32"
    },
    "lp_msp_val": {
        "offset": str(int(bootcpucfg_start_pos+bootcpucfg_len*bootcpucfg_lp_index)+20),
        "pos": "0",
        "bitlen": "32"
    },
    # boot2 config
    "boot2_pt_table_0": {
        "offset": str(int(boot2_start_pos)+0),
        "pos": "0",
        "bitlen": "32"
    },
    "boot2_pt_table_1": {
        "offset": str(int(boot2_start_pos)+4),
        "pos": "0",
        "bitlen": "32"
    },
    # flash config table
    "flashCfgTableAddr": {
        "offset": str(int(flashcfg_table_start_pos)+0),
        "pos": "0",
        "bitlen": "32"
    },
    "flashCfgTableLen": {
        "offset": str(int(flashcfg_table_start_pos)+4),
        "pos": "0",
        "bitlen": "32"
    },
    # patch config
    "patch_read_addr0": {
        "offset": str(int(patch_on_read_start_pos)+0),
        "pos": "0",
        "bitlen": "32"
    },
    "patch_read_value0": {
        "offset": str(int(patch_on_read_start_pos)+4),
        "pos": "0",
        "bitlen": "32"
    },
    "patch_read_addr1": {
        "offset": str(int(patch_on_read_start_pos)+8),
        "pos": "0",
        "bitlen": "32"
    },
    "patch_read_value1": {
        "offset": str(int(patch_on_read_start_pos)+12),
        "pos": "0",
        "bitlen": "32"
    },
    "patch_read_addr2": {
        "offset": str(int(patch_on_read_start_pos)+16),
        "pos": "0",
        "bitlen": "32"
    },
    "patch_read_value2": {
        "offset": str(int(patch_on_read_start_pos)+20),
        "pos": "0",
        "bitlen": "32"
    },
    "patch_read_addr3": {
        "offset": str(int(patch_on_read_start_pos)+24),
        "pos": "0",
        "bitlen": "32"
    },
    "patch_read_value3": {
        "offset": str(int(patch_on_read_start_pos)+28),
        "pos": "0",
        "bitlen": "32"
    },
    "patch_jump_addr0": {
        "offset": str(int(patch_on_jump_start_pos)+0),
        "pos": "0",
        "bitlen": "32"
    },
    "patch_jump_value0": {
        "offset": str(int(patch_on_jump_start_pos)+4),
        "pos": "0",
        "bitlen": "32"
    },
    "patch_jump_addr1": {
        "offset": str(int(patch_on_jump_start_pos)+8),
        "pos": "0",
        "bitlen": "32"
    },
    "patch_jump_value1": {
        "offset": str(int(patch_on_jump_start_pos)+12),
        "pos": "0",
        "bitlen": "32"
    },
    "patch_jump_addr2": {
        "offset": str(int(patch_on_jump_start_pos)+16),
        "pos": "0",
        "bitlen": "32"
    },
    "patch_jump_value2": {
        "offset": str(int(patch_on_jump_start_pos)+20),
        "pos": "0",
        "bitlen": "32"
    },
    "patch_jump_addr3": {
        "offset": str(int(patch_on_jump_start_pos)+24),
        "pos": "0",
        "bitlen": "32"
    },
    "patch_jump_value3": {
        "offset": str(int(patch_on_jump_start_pos)+28),
        "pos": "0",
        "bitlen": "32"
    },
    # rsvd config
    "reserved1": {
        "offset": str(int(rsvd_start_pos)+0),
        "pos": "0",
        "bitlen": "32"
    },
    "reserved2": {
        "offset": str(int(rsvd_start_pos)+4),
        "pos": "0",
        "bitlen": "32"
    },
    "reserved3": {
        "offset": str(int(rsvd_start_pos)+8),
        "pos": "0",
        "bitlen": "32"
    },
    "reserved4": {
        "offset": str(int(rsvd_start_pos)+12),
        "pos": "0",
        "bitlen": "32"
    },
    "reserved5": {
        "offset": str(int(rsvd_start_pos)+16),
        "pos": "0",
        "bitlen": "32"
    },
    "crc32": {
        "offset": str(int(crc32_start_pos)+0),
        "pos": "0",
        "bitlen": "32"
    },
}
