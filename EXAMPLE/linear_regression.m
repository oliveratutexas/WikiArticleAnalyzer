data = load('cricket_chirps_versus_temperature.txt');

x = data(:,2);
y = data(:,1);

function plotData(x,y)
	plot(x,y,'rx','MarkerSize',8);
end

%initial plot
plotData(x,y);

xlabel('Rate of Crickets Chirping')
ylabel('Temperature of Degrees in Farenheight');
fprintf('Program Paused, press enter to continue');
pause;

m = length(x);
X = [ones(m,1) x];

% Calculate theta
theta = (pinv(X'*X))*X'*y;

hold on;
legend('Training Data', 'Linear Regression');
plot(X(:,2),X * theta, '-');

hold off;
pause;
