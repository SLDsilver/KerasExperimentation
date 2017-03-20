%Resolve prior variables 
clc;
clear;

%Run the function
answer = read_complex_binary('samples.dat', 100000);

%Write to another file
fileID = fopen('usabledata.txt', 'wt');
for i = 1:999999
    fprintf(fileID, '%f + %fi\n', answer(i), answer(i)/1i);
end
fclose(fileID);
