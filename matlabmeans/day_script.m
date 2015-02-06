%% Script 

clc
clear all
close all

%% Creating Dynamic Path:

folder = '/home/isman7/BeeCounter';
path1  = '/BeeCounter2014-08-';

% BeeCounter2014-07-24T13_01.csv

dia_ini  = 4;
hora_ini = 00; 
min_ini  = 00;

dia_fin  = 4;
hora_fin = 23; 
min_fin  = 59;



path2 = '.csv';

pos = 10; %Primera = 1;

in_out = 2;
%in = 1, out = 2

d = (pos-1)*2 + in_out;

OneDaySensor = fopen('OneDaySensor.csv', 'w');

for dia_i = dia_ini:dia_fin

for hora_i = hora_ini:hora_fin

for min_i = min_ini:min_fin

    if (hora_i <10) path  = [folder, path1, '0', num2str(dia_i), 'T0', num2str(hora_i), '_']; 
    else            path  = [folder, path1, '0', num2str(dia_i), 'T',  num2str(hora_i), '_']; 
    end
    
    if (min_i <10)  path = [path, '0', num2str(min_i), path2];
    else            path = [path,      num2str(min_i), path2];
    end

% Reading data from one file (one minute)
path

try 
    DATAf  = fopen(path);
    if DATAf == -1
          error(['Not file founded at:', path]),
          
          
    else
        
    DATAs  = textscan(DATAf, '%s');
    DATAs  = DATAs{1};
    lenD   = length(DATAs);

    oneminDATA = zeros(lenD,2);

    for ii = 1:lenD
    % Time calculus:
    oneminDATA(ii, 1) = (((str2double(DATAs{ii}(18:26))/60) + str2double(DATAs{ii}(15:16)))/60) + str2double(DATAs{ii}(12:13)) + ((dia_i - dia_ini)*24); %(((s/60)+min)/60) + h
    % Value conversion: 
    % oneminDATA(ii, 2) = str2double(DATAs{ii}(30+3*d:32+3*d));
    
    finder = find(DATAs{ii} == ',');
    fd1 = finder(d+1) +1; 
    fd2 = finder(d+2) -1;
    oneminDATA(ii, 2) = str2double(DATAs{ii}(fd1:fd2));
    
    
    %Writing
    fprintf(OneDaySensor, '%f; ', oneminDATA(ii,1));
    fprintf(OneDaySensor, '%d\n', oneminDATA(ii,2));
    
    
    end

    fclose(DATAf);
        
        
    end
    
catch Ex
    
    disp('Can not read file') 
    
    
end
    





end

min_ini = 0;


end

hora_ini = 0;

end
fclose(OneDaySensor);




