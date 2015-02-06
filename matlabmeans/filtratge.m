%% Script filtratge

close all

DATAdia(:,1) = OneDaySensor_4A(:,1)*3600;
DATAdia(:,2) = 100 * (3000 - OneDaySensor_4A(:,2))/ 3000;


% Suma cada minut

% Cada segon aproximadament son 4 punts. Cada minut son 240. 

npunts = 240; % 240 p -> 1 min

mean60s = zeros(1, floor(length(DATAdia)/npunts) );


for ii = 1:length(mean60s)-2
   
    mean60s(ii) = sum(DATAdia(npunts*(ii):npunts*(ii+2),2))/(2*npunts);
    
    
end


npunts = 120; % 120 p -> 30 segs

mean30s = zeros(1, floor(length(DATAdia)/npunts) );


for ii = 1:length(mean30s)-2
   
    mean30s(ii) = sum(DATAdia(npunts*(ii):npunts*(ii+2),2))/(2*npunts);
    
    
end


npunts = 60; % 120 p -> 15 segs

mean15s = zeros(1, floor(length(DATAdia)/npunts) );


for ii = 1:length(mean15s)-2
   
    mean15s(ii) = sum(DATAdia(npunts*(ii):npunts*(ii+2),2))/(2*npunts);
    
    
end


figure(2), 


subplot(2,2, 1), plot(DATAdia(1:end-2,1)/3600, DATAdia(1:end-2,2)), axis([0, 24, 0, 100]), xlabel('4 agost 2014 (hores)'),
subplot(2,2, 2), plot(mean15s), axis([0, 6000, 0, 100]), xlabel('Promig per cada 15s'),
subplot(2,2, 3), plot(mean30s), axis([0, 3000, 0, 100]), xlabel('Promig per cada 30s'),
subplot(2,2, 4), plot(mean60s), axis([0, 1500, 0, 100]), xlabel('Promig per cada 60s'),


