%Resolve prior variables 
clc;
clear;

filename = 'samples.dat';
num_points = 1000000;
desired_output = 'usabledata.txt';

%Run the function
answer = read_complex_binary(filename, num_points);

%Write to another file
fileID = fopen(desired_output, 'wt');
for i = 1:num_points
    fprintf(fileID, '%f + %fi\n', answer(i), answer(i)/1i);
end
fclose(fileID);
