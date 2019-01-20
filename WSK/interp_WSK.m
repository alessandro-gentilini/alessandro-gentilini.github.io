function y = interp_WSK(samples,T_s,t)
  y = zeros(1,length(t));
  for k = 1:1:length(samples)
    % https://en.wikipedia.org/wiki/Whittaker%E2%80%93Shannon_interpolation_formula
    % the above formula uses so called "normalized sinc", i.e. sin(pi*x)/(pi*x)
    y+=samples(k)*sin(pi*(t-k*T_s)/T_s)./(pi*(t-k*T_s)/T_s);
  endfor
endfunction
