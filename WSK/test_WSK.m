f=1;
T=1/f;
mysignal = @(t) sin(2*pi*f*t);

f_s=16*f; % sampling rate
T_s=1/f_s; % sampling period
t=0:T_s:T; % times at which mysignal is sampled 
t1=linspace(0,T,100); % times to plot mysignal "continuosly"

% plot mysgnal as a "continuos" signal
hold off;
plot(t1,mysignal(t1),'r')
hold on;

function y = Whittaker_Shannon_interpolation(samples,T_s,t)
% samples are the samples of the original signal;
% T_s is sampling period;
% t are the times at which interpolate the original signal;
% y are the interpolated values (reconstructed) of the original signal at times t.
  y = zeros(1,length(t));
  normalized_sinc = @(x) sin(pi*x)./(pi*x);
  for k = 1:1:length(samples)
    % https://en.wikipedia.org/wiki/Whittaker%E2%80%93Shannon_interpolation_formula
    % the above formula uses so called "normalized sinc", i.e. sin(pi*x)/(pi*x)
    y+=samples(k)*normalized_sinc((t-(k-1)*T_s)/T_s);
  endfor
endfunction

samples=mysignal(t);
stem(t,samples,'b')
hold on;

y=Whittaker_Shannon_interpolation(samples,T_s,t1);
plot(t1,y,'k-o')

legend('original signal','samples','reconstructed')

figure
plot(t1,mysignal(t1)-y)