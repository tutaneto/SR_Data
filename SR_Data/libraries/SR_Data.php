<?php
    // variables: user, pw, file, template, symbol
    $symbol   = $_GET['symbol'];
    $template = $_GET['template'];
    $user   = $_SESSION["userid"];
    $passwd = $_SESSION["userpw"];

    // IT NEEDS TO TREAT THE ERRORS

    $file_path       = '../wwwsec/output/';
    $file_name_queue = $file_path . 'queue.txt';
    $file_name_base  = $file_path . 'out';
    $file_name_extra = $file_path . 'extra';

    $sleep_time = 200 * 1000;  // 200ms
    $timeOut = 30 * 1000000 / $sleep_time; // 30s

    # Delay menor para máquina loca (Alessandro)
    if (file_exists("/home/user/work/php-workspace/"))
        $timeOut = 10 * 1000000 / $sleep_time; // 10s

    // increment pos_in
    $fp = fopen($file_name_queue, 'c+');            // open
    flock($fp, LOCK_EX);                            // lock
    fscanf ($fp, "%d %d", $pos_in, $pos_out);       // read
    ftruncate($fp, 0);                              // clean
    fseek($fp, 0);                                  // position
    $pos_in++;                                      // increment
    fprintf($fp, "%d %d", $pos_in, $pos_out);       // write
    fflush($fp);                                    // flush
    flock($fp, LOCK_UN);                            // unlock
    fclose($fp);                                    // close
    clearstatcache();                               // clear cache

    // saves symbol name
    $fp = fopen(($file_name_base . '_' . $pos_in . '.txt'), 'w');
    fprintf($fp, '%s', $symbol);
    fflush($fp);
    fclose($fp);

    rename(($file_name_extra      . $fileNum . '.csv'),
           ($file_name_base . '_' . $pos_in  . '.ext'));

    # rename out????.csv file (última coisa a ser feita, esse arquivo é esperado do outro lado)
    // $fileNum = '';
    rename(($file_name_base . ''  . $fileNum . '.csv'),  // $fileNum comes from "father"
           ($file_name_base . '_' . $pos_in  . '.csv'));

    // graphic file
    $file_name_png = ($file_name_base . '_' . $pos_in . '.png');

    // waits execution
    $cycles = 0;
    while(!file_exists($file_name_png)) {
        usleep($sleep_time);
        clearstatcache();
        $cycles++;
        if ($cycles > $timeOut) {
            print('<h2 style="color:red">Falha por timeout<h2>');
            die;
        }
    }

    // show image
    printf('<a href="' . $file_name_png . '" download rel="noopener noreferrer" target="_blank">Download</a><br>');
    // printf('<a href=""' . ' download="' . $file_name_png . '" rel="noopener noreferrer" target="_blank">Download</a><br>');
    printf('<img id="genimage" src="' . $file_name_png . '?rnd=' . rand() . '" alt=' . $symbol . '><br>');

    exit;
?>