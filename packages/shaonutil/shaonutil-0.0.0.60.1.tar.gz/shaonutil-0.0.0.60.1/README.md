# Shaonutil  - 0.0.0.55.1
## Utility Functions for Developers

Stable Version - 0.0.0.55.1<br>
Author: Shaon Majumder<br>
Contact: smazoomder@gmail.com

## Area of Utilities

- file
- image
- imgcode
- mysqlDB
- network
- os
- process
- stats
- strings
- windows

## Installation
<code>pip install shaonutil</code>

## Function Usages

### File
Function **get_all_dirs()**<br>
Function **get_all_files_dirs()**<br>
Function **package_exists(package_name)** -> Description: check if a python pcakage exists.<br>
Function **pip_install(package_name)**<br>
Function **get_all_functions(object)** -> Description: shaonutil.file.get_all_functions(object/file/class)<br>
Function **ConfigSectionMap(Config,section)**<br>
Function **read_configuration_ini(filename)**<br>
Function **read_safecase_configuration_ini(filename)**<br>
Function **write_configuration_ini(configs_par,filename,f_mode)**<br>
Function **read_json(filename)** -> Description: Read JSON file and return dictionary<br>
Function **write_json(obj,filename)** -> Description: Write JSON file<br>
Function **read_file(filename)** -> Description: Read File and return lines as list<br>
Function **write_file(filename,strs,mode)** -> Description: Write File from string<br>
Function **read_pickle(filename)**<br>
Function **write_pickle(filename,obj_)**<br>
Function **open_file_with_default_app(filepath)**<br>
Function **get_last_file_of_dir(filename)**<br>
Function **remove_duplicateLines_from_file(filename)**<br>
Class **CaseConfigParser**<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **optionxform(optionstr)**<br>
### Image
Function **svg2img(infile,outfile)**<br>
Function **svg2pdf(infile,outfile)**<br>
Function **change_image_size_ratio(img_name,out_name,percent)**<br>
Function **draw_text(img,text,fnt_name,fnt_size)**<br>
Function **merge_horizontally(images,filename)**<br>
Function **merge_vertically(images,filename)**<br>
Function **give_screenshot_caption(img_name,text,fnt_path)**<br>
### BarCode
Function **calculate_checksum(data)** -> Description: Calculates the checksum for EAN13-Code / EAN8-Code return type: Integer<br>
Function **verify_data(data)** -> Description: Verify the EAN encoded data<br>
Function **actual_data(decodedObjects)** -> Description: Returns data without checksum digit for EAN type<br>
Function **encode(type_,file_,data,rt)** -> Description: Encode the data as barcode or qrcode<br>
Function **decode(infile,log)** -> Description: Decode barcode or qrcode<br>
Function **markBarcode(im,decodedObjects)** -> Description: Mark and show the detected barcode<br>
Function **make_barcode_matrix(type_,unique_ids,row_number,column_number,filename)** -> Description: Make barcode matrix image<br>
Function **read_live_barcode(detection_threshold)** -> Description: Live read the barcode and returns data<br>
### Mysql Database
Function **create_configuration(option,file_name)** -> Description: Creating Configuration<br>
Function **remove_aria_log(mysql_data_dir)** -> Description: Removing aria_log.### files to in mysql data dir to restart mysql<br>
Function **get_mysql_datadir(mysql_bin_folder,user,pass_)** -> Description: Get mysql data directory<br>
Class **MySQL** -> Description: A class for all mysql actions<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **__init__(config,init_start_server,log)**<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **start_mysql_server()** -> Description: Start mysql server<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **stop_mysql_server(force)** -> Description: Stop MySQL Server<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **reopen_connection()** -> Description: reopen<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **close_connection()** -> Description: closing the connection<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **config()**<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **config(new_value)**<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **filter_config()**<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **make_cursor()**<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **is_mysql_user_exist(mysql_username)** -> Description: check if mysql user exist return type:boolean<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **listMySQLUsers()** -> Description: list all mysql users<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **createMySQLUser(host,userName,password,querynum,updatenum,connection_num)** -> Description: Create a Mysql User<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **grantMySQLUserAllPrivileges(host,userName,querynum,updatenum,connection_num)** -> Description: Grant a user all privilages<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **is_db_exist(dbname)** -> Description: Check if database exist<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **create_db(dbname)** -> Description: Create Database<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **delete_db(dbname)** -> Description: Delete Database<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **get_databases()** -> Description: Get databases names<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **create_table(tbname,column_info)** -> Description: Create a table under a database<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **delete_table(tbname)** -> Description: Delete a table under a database<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **get_tables()** -> Description: Get table names<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **describe_table(tbname)** -> Description: Describe a table structure<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **is_table_exist(tbname)** -> Description: Check if table exist<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **get_columns(tbname)** -> Description: Get column names of a table<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **show_table(tbname)**<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **get_unique_id_from_field(field_name,key_length,filters)** -> Description: Get a random unique id not registered in a specific field<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **delete_row(delete_dict)** -> Description: Delete a row of data<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **insert_row(value_tupple)** -> Description: Insert row of data<br>
### Network
Function **url_encoding_to_utf_8(url)** -> Description: url_encoding_to_utf_8(url)<br>
Function **check_valid_url(url)**<br>
Class **Email**<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **__init__()**<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **authentication()**<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **authentication(new_value)**<br>
&nbsp;&nbsp;&nbsp;&nbsp;Function **send_email(receiver_address,subject,mail_content,attachment_file_link,log)**<br>
### Process
Function **is_process_exist(process_name)**<br>
Function **kill_duplicate_process(process_name,log)** -> Description: Kill a process if there is more than one instance is running.<br>
Function **killProcess_ByAll(PROCNAME)**<br>
Function **killProcess_ByPid(pid)**<br>
Function **list_processes(sort,save_file,log)**<br>
Function **computer_idle_mode()**<br>
Function **obj_details_dump(obj)** -> Description: check dump<br>
### Statistics
Function **counter(li,number)**<br>
Function **occurance_dic(li)**<br>
Function **mean(li)** -> Description: Avearage or mean of elements - shaonutil.stats.mean(list of numbers)<br>
Function **median(li)** -> Description: Median of elements - shaonutil.stats.median(list of numbers)<br>
Function **mode(li)** -> Description: Mode of elements - shaonutil.stats.mode(list of numbers)<br>
### String
Function **nicely_print(dictionary,print)** -> Description: Prints the nicely formatted dictionary - shaonutil.strings.nicely_print(object)<br>
Function **change_dic_key(dic,old_key,new_key)** -> Description: Change dictionary key with new key<br>
Function **randomString(stringLength)** -> Description: Generate a random string of fixed length <br>
Function **generateSecureRandomString(stringLength)** -> Description: Generate a secure random string of letters, digits and special characters <br>
Function **generateCryptographicallySecureRandomString(stringLength,filters)** -> Description: Generate a random string in a UUID fromat which is crytographically secure and random<br>
### Windows
Function **is_winapp_admin()**<br>
Function **get_UAC_permission(func)**<br>


Function Usages End


## Versioning 

*major.minor[.maintenance[.build]]* (example: *1.4.3.5249*)

adoption: major.minor.patch.maintenance.status.trials_for_success

The last position

- 0 for alpha (status) 
- 1 for beta (status)
- 2 for release candidate
- 3 for (final) release

For instance:

- 1.2.0.1 instead of 1.2-a1
- 1.2.1.2 instead of 1.2-b2 (beta with some bug fixes)
- 1.2.2.3 instead of 1.2-rc3 (release candidate)
- 1.2.3.0 instead of 1.2-r (commercial distribution)
- 1.2.3.5 instead of 1.2-r5 (commercial distribution with many bug fixes)