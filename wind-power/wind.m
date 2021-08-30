df = csvread('wind_data.csv');
df = df(:,3:12);

df(any(isnan(df),2),:) = []; 

%df = df(2:end,:);

p = df(:,1);

W1 = circshift(df(:,2:4), 1);
W2 = circshift(df(:,5:7), 2);
W3 = circshift(df(:,8:10), 3);

% W = [p(3:end),W1(3:end),W2(3:end),W3(3:end)];

p = p(3:end);
W1 = W1(3:end,:);

[xq,yq] = meshgrid(0:1:30, 0:10:359);

vq = griddata(W1(:,1),W1(:,2),p,xq,yq);

idx = randperm(length(W1));
N = 1000

W1_ = W1(idx(1:N), 1:3);
p_ = p(idx(1:N));

surf(xq,yq,vq)

hold on

plot3(W1_(:,1),W1_(:,2),p_,'x')
xlabel('Velocity (m/s)')
ylabel('Direction (degrees)')
zlabel('Power (kW)')