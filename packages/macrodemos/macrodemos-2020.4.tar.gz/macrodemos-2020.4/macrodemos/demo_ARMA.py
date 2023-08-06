"""
demo_ARMA: Module for learning about  ARMA processes

This module provides a single function, ARMA_demo(), which creates a dash consisting of 7 plots to study the
theoretical properties of ARMA(p, q) process, as well as their estimated counterparts. The plots display
    1. a simulated sample
    2. autocorrelations
    3. partial autocorrelations
    4. impulse response function
    5. spectral density
    6. AR inverse roots
    7. MA inverse roots

Randall Romero Aguilar
2016-2020
"""


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import webbrowser

import numpy as np
from numpy.polynomial import Polynomial as P
import pandas as pd
from scipy import signal

from statsmodels.tsa.arima_model import ARMA as tsaARMA # PARA ESTIMAR MODELO
from statsmodels.tsa.arima_process import ArmaProcess # MODELO TEORICO
from statsmodels.tsa.stattools import acf, pacf # autocorrelation and partial autocorrelation


# Esta parte controla asuntos de estética de la página
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': 'SteelBlue',
    'text': 'White',
    'controls': '#DDDDDD',
    'buttons': 'Orange'
}

# Esta función se utiliza para calcular la varianza del proceso ARMA


def qnwsimp(n, a, b):
    """
    Compute univariate Simpson quadrature nodes and weights

    Parameters
    ----------
    n : int, the number of nodes
    a : int, the lower endpoint
    b : int, the upper endpoint

    Returns
    -------
    nodes : np.ndarray(dtype=float)
        An n element array of nodes

    weights : np.ndarray(dtype=float)
        An n element array of weights

    Notes
    -----
    Based of original function ``qnwsimp1`` in CompEcon toolbox by
    Miranda and Fackler

    References
    ----------
    Miranda, Mario J, and Paul L Fackler. Applied Computational
    Economics and Finance, MIT Press, 2002.

    """
    if n % 2 == 0:
        print("WARNING qnwsimp: n must be an odd integer. Increasing by 1")
        n += 1

    nodes = np.linspace(a, b, n)
    weights = np.tile([2.0, 4.0], [int((n + 1) / 2)])
    weights = weights[:n]
    weights[0] = weights[-1] = 1
    weights *= (b-a) / (3*(n-1))

    return nodes, weights


def validate_lists_of_values(value: str):
    """Splits AR and MA string into list of floats    """
    return [float(x) for x in value.split(',')] if value else None


#=======================================================================================================================
#
#  ARMA CLASS
#
#_______________________________________________________________________________________________________________________
class ARMA(ArmaProcess):
    def __init__(self, c=0, phi=None, theta=None, sigma2=1.0, nobs=120):
        if type(phi) is np.ndarray:
            ar = np.r_[1, -phi]  # add zero-lag and negate
        elif phi in (None, 0, ''):
            ar = np.ones(1)
        else:
            ar = np.r_[1, -np.array(phi)]  # add zero-lag and negate

        if type(theta) is np.ndarray:
            ma = np.r_[1, theta]  # add zero-lag
        elif theta in (None, 0, ''):
            ma = np.ones(1)
        else:
            ma = np.r_[1, np.array(theta)]  # add zero-lag

        super().__init__(ar, ma, nobs)
        self.c = float(c)  # intercept
        self.Phi = P(self.ar) # AR polynomial
        self.Theta = P(self.ma)  # MA polynomial
        self.p = self.Phi.degree()
        self.q = self.Theta.degree()
        self.sigma2 = float(sigma2)  # white noise variance
        self.simulated_data = None
        self.show_estimates = False
        self.estimates = {'repr': ''}
        self.estimated = False



    @property
    def mean(self):
        return self.c / self.Phi(1) if self.isstationary else np.nan

    @property
    def variance(self):
        frequencies, weights = qnwsimp(121, 0, np.pi)
        sw = self.periodogram(frequencies)
        return 2* weights.dot(sw)

    def __simulate_shocks(self, n, irf=False):
        if irf:
            shocks = np.zeros(n, float)
            shocks[0] = 1.0
        else:
            shocks = np.random.randn(n) * np.sqrt(self.sigma2)
        return shocks

    def __simulate_MA(self, e):
        #return np.convolve(self.Theta.coef[::-1], e, 'valid')
        return np.convolve(self.ma[::-1], e, 'valid')

    def __simulate_AR(self, e):
        p = self.p
        y0 = np.zeros(p)
        if self.isstationary:
            y0 += self.mean

        phi = self.arcoefs[::-1]
        y = np.hstack((y0, np.zeros_like(e)))

        for t, et in enumerate(e):
            y[t + p] = self.c + phi.dot(y[t:(t+p)]) + et
        return y

    def sample(self, n=101):
        e = self.__simulate_shocks(n + self.q)
        ma = self.__simulate_MA(e)
        self.simulated_data = pd.Series(self.__simulate_AR(ma))

    #def sample(self, n=101):
    #    raw_data = self.generate_sample(nsample=n, scale=np.sqrt(self.sigma2))
    #    print(raw_data)
    #    self.simulated_data = pd.Series(raw_data + self.mean)

    def estimate(self, p, q):
        try:
            res = tsaARMA(self.simulated_data.values, order=[p, q]).fit()
            self.estimates = {'c': res.params[0], 'phi': res.arparams, 'theta': res.maparams}
            self.estimates['repr'] = str(ARMA(self.estimates['c'], self.estimates['phi'], self.estimates['theta']))
            self.estimates['fitted'] = pd.Series(res.fittedvalues)
            self.estimates['arroots'] = np.array([1/x for x in res.arroots])
            self.estimates['maroots'] = np.array([1 / x for x in res.maroots])
            self.estimated = True
        except:
            self.estimated = False
            self.estimates['repr'] = 'The model could not be estimated'

    def print2moments(self):
        return f'$E(y_t) = {self.mean:g}, V(y_t) = {self.variance:g}$' if self.isstationary else 'This process is not stationay!'


    def __str__(self):
        c = f'{self.c:g}' if self.c else ''
        if self.p:
            ar = ' '.join([f'{phi:+g}y_{{t-{k+1}}}' for k, phi in enumerate(self.arcoefs) if phi])
        else:
            ar = ''
        if self.q:
            ma = ' '.join([f'{theta:+g}\epsilon_{{t-{k+1}}}' for k, theta in enumerate(self.macoefs) if theta])
        else:
            ma = ''

        return r'$y_t = ' + c + ar + ' + \epsilon_t' + ma + '$'

    def periodogram(self, frecuencias):
        return abs(signal.freqz(self.ma, self.ar, worN=frecuencias)[1]) ** 2 / (2 * np.pi)

    def plot_spectral(self):
        results = {'layout': {'title': 'Spectral Density'}}
        if self.isstationary:
            results['data'] = [{'x': omega, 'y': self.periodogram(omega), 'type': 'line', 'name': 'actual', 'fill': 'tozeroy'}]
        else:
            results['data'] = [{'x': omega, 'y': np.zeros_like(omega), 'type': 'line', 'name': 'not defined'}]
        if self.show_estimates:
            yy = self.simulated_data - self.simulated_data.mean()
            v = (yy ** 2).mean()  # estimated variance
            T = yy.size
            r = int(np.sqrt(T))
            gamma = acf(yy, unbiased=False, nlags=r, fft=False)
            k = np.arange(r + 1)
            g = 1 - k / r # Bartlett window
            sw = ((np.cos(np.outer(omega, k)) * (g * gamma)).sum(axis=1) * 2 - 1)
            sw *= v / (2 * np.pi)  # rescale
            results['data'].append({'x': omega, 'y': sw, 'type': 'line', 'name': 'estimated'})

        return results

    def plot_correlogram(self, lags):
        results = dict()
        results['layout'] = {'title': 'Autocorrelations'}

        if self.isstationary:
            results['data'] = [{'y': self.acf(lags=lags), 'type': 'bar', 'name': 'actual'}]
        else:
            results['data'] = [{'y': np.zeros(lags), 'type': 'bar', 'name': 'not defined'}]

        if self.show_estimates:
            self.estimates['acf'] = acf(self.simulated_data, unbiased=True, nlags=lags, fft=False)
            results['data'].append({'y': self.estimates['acf'], 'type': 'bar', 'name': 'estimated'})

        return results

    def plot_partial_correlogram(self, lags):
        results = dict()
        results['layout'] = {'title': 'Partial Autocorrelations'}

        if self.isstationary:
            results['data'] = [{'y': self.pacf(lags=lags), 'type': 'bar', 'name': 'actual'}]
        else:
            results['data'] = [{'y': np.zeros(lags), 'type': 'bar', 'name': 'not defined'}]

        if self.show_estimates:
            self.estimates['pacf'] = pacf(self.simulated_data, nlags=lags)
            results['data'].append({'y': self.estimates['pacf'], 'type': 'bar', 'name': 'estimated'})

        return results

    def plot_process(self):
        y = self.simulated_data.values
        t = np.arange(y.size)
        results = dict()
        results['data'] = [{'x': t, 'y': y, 'type': 'line','name': 'actual'},
                           {'x': [0, t[-1]], 'y': [self.mean, self.mean], 'type':'line','name':r'$\mu$'}]
        results['layout'] = {'title': 'Simulated Data'}
        if self.show_estimates and self.estimated:
            results['data'].insert(1, {'x': t, 'y': self.estimates['fitted'], 'type': 'line','name': 'fitted'})

        """process = go.Figure()
        process.add_trace(go.Scatter(x=t, y=y, name='actual'))
        if self.show_estimates and self.estimated:
            process.add_trace(go.Scatter(x=t, y=self.estimates['fitted'], name='fitted'))
        process.add_trace(go.Scatter(x=[0, t[-1]], y=[self.mean, self.mean], name=r'$\mu$'))
        process.update_layout(title_text='Simulated Data')
        """
        return results #process

    def plot_ar_roots(self):
        results = dict()

        if self.p:
            roots = 1/self.arroots #statsmodels gives roots of the lag polinomial, not the characteristic function
            radium = np.abs(roots)
            angles = np.angle(roots, True)
            results['data'] = [{'r': radium, 'theta': angles, 'type': 'scatterpolar','mode': 'markers', 'marker': {'size': 16}, 'name': 'actual'}]
        else:
            radium = np.ones(2)
            results['data'] = [{'r': [0], 'theta': [0], 'type': 'scatterpolar','mode': 'markers','marker': {'size': 1}, 'name': 'Actual'}]

        if self.show_estimates and self.estimated:
            roots = self.estimates['arroots']
            if len(roots):
                radium2 = np.abs(roots)
                angles2 = np.angle(roots, True)

                results['data'].append(
                    {'r': radium2, 'theta': angles2, 'type': 'scatterpolar', 'mode': 'markers', 'marker': {'size': 16},
                     'name': 'estimated'})
            else:
                radium2 = np.ones(2)
        else:
            radium2 = np.ones(2)

        maxr = max([1, radium.max(), radium2.max()])
        results['layout'] = {'title': 'AR inverse roots',
                             'polar': {'angularaxis': {'thetaunit': 'radians', 'dtick': np.pi / 4},
                                       'radialaxis': {'tickvals': [0.0, 1.0], 'range': [0, maxr]}}
                             }

        return results

    def plot_ma_roots(self):
        results = dict()

        if self.q:
            roots = 1/self.maroots #statsmodels gives roots of the lag polinomial, not the characteristic function
            radium = np.abs(roots)
            angles = np.angle(roots, True)
            results['data'] = [{'r': radium, 'theta': angles, 'type': 'scatterpolar','mode': 'markers', 'marker': {'size': 16}, 'name': 'actual'}]
        else:
            radium = np.ones(2)
            results['data'] = [{'r': [0], 'theta': [0], 'type': 'scatterpolar','mode': 'markers','marker': {'size': 1}, 'name': 'Actual'}]

        if self.show_estimates and self.estimated:
            roots = self.estimates['maroots']
            if len(roots):
                radium2 = np.abs(roots)
                angles2 = np.angle(roots, True)

                results['data'].append(
                    {'r': radium2, 'theta': angles2, 'type': 'scatterpolar', 'mode': 'markers', 'marker': {'size': 16},
                     'name': 'estimated'})
            else:
                radium2 = np.ones(2)
        else:
            radium2 = np.ones(2)

        maxr = max([1, radium.max(), radium2.max()])
        results['layout'] = {'title': 'MA inverse roots',
                             'polar': {'angularaxis': {'thetaunit': 'radians', 'dtick': np.pi / 4},
                                       'radialaxis': {'tickvals': [0.0, 1.0], 'range': [0, maxr]}}
                             }

        return results

    def plot_irf(self, horizon):
        y = self.impulse_response(horizon)
        x = np.arange(y.size)
        result = dict()
        result['data'] = [{'x': x, 'y': y, 'type': 'bar', 'name': 'actual'}]
        result['layout'] = {'title': 'Impulse Response Function'}

        if self.show_estimates and self.estimated:
            temp = ARMA(self.estimates['c'], self.estimates['phi'], self.estimates['theta']).impulse_response(horizon)
            x = np.arange(temp.size)
            result['data'].append({'x': x, 'y': temp, 'type': 'bar', 'name': 'estimated'})
        return result



#=======================================================================================================================
#
#  APP STARTS HERE
#
#_______________________________________________________________________________________________________________________
mathjax = ["https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML"]  # to display math
omega = np.linspace(0, np.pi, 121)  # frequencies for spectral plot

def app_parameter(label, appid, inputtype, value, size='20'): # to make input parameter
    return html.Th(label), html.Th(dcc.Input(id=appid, type=inputtype, value=value, size=size))

def app_parameter_row(label, appid, inputtype, value, size='20'): # to make input parameters
    return html.Tr([*app_parameter(label, appid, inputtype, value, size)])


app = dash.Dash(__name__,external_stylesheets=external_stylesheets, external_scripts=mathjax)  # main application


#======DESIGN THE APP===============

app.layout = html.Div(children=[
    html.H2(id='title',
            style={'textAlign': 'center', 'color': colors['text']}),
    html.P(id='estimated',
            style={'textAlign': 'center', 'color': colors['text']}),
    html.Div(children=[html.H4("ARMA Parameters"),
                       html.Table(children=[
                           app_parameter_row('c', 'c', 'number', 0),
                           app_parameter_row('AR', 'AR', 'text', ''),
                           app_parameter_row('MA', 'MA', 'text', ''),
                           app_parameter_row('V[e]', 'vare', 'number', 1.0)],
                       ),
                       html.Hr(),
                       html.H5(id='moments'),
                       html.H4("Figure Parameters"),
                       html.Table(children=[
                           app_parameter_row('Periods', 'periods', 'text', 120, '8'),
                           app_parameter_row('AC-lags', 'lags', 'text', 12, '8'),
                           app_parameter_row('IRF horizon', 'horizon', 'text', 24, '8'),
                           html.Tr([html.Th('Show estimates'),
                                    html.Th(dcc.RadioItems(id='showestimates',
                                                         options=[{'label': 'Yes', 'value': 'Yes'}, {'label': 'No', 'value': 'No'}],
                                                         value='No'))]),
                       ],
                       ),
                       html.Div(id='p,q', children = [html.Tr([*app_parameter('p', 'p', 'text', '0', '5'),
                                                               *app_parameter('q', 'q', 'text', '0', '5')])]),
                       html.Hr(),
                       html.Button('PLOT', id='execute',style={'textAlign': 'center', 'backgroundColor': colors['buttons']}),
                       html.P('ARMA PROCESS DEMO', style={'textAlign': 'center', 'color': colors['text'],'marginTop':500}),
                       ],
             style={'textAlign': 'center', 'color': colors['controls'], 'width': '20%', 'display': 'inline-block'}),

    html.Div(style={'width': '80%', 'float': 'right', 'display': 'inline-block'},
             children=[
                 # --PLOT 1:  SIMULATED TIME SERIES----------------------------------------------------------------------
                 dcc.Graph(id='plot-process',
                           style={'width': '99%', 'float': 'left', 'display': 'inline-block'}),
                 #--PLOT 2a:  AUTOCORRELOGRAM---------------------------------------------------------------------------
                 dcc.Graph(id='plot-correlogram',
                           style={'width': '33%', 'float': 'left', 'display': 'inline-block'}),
                 #--PLOT 2b:  PARCIAL AUTOCORRELOGRAM---------------------------------------------------------------------------
                 dcc.Graph(id='plot-partial-correlogram',
                           style={'width': '33%', 'float': 'left', 'display': 'inline-block'}),
                 # --PLOT 2c:  IMPULSE RESPONSE FUNCTION----------------------------------------------------------------
                 dcc.Graph(id='plot-irf',
                           style={'width': '33%', 'float': 'left', 'display': 'inline-block'}),
                 #--PLOT 2a:  SPECTRAL DENSITY--------------------------------------------------------------------------
                 dcc.Graph(id='plot-spectrum',
                           style={'width': '39%', 'float': 'left', 'display': 'inline-block'}),
                 #--PLOT 3a:  AR ROOTS----------------------------------------------------------------------------------
                 dcc.Graph(id='plot-ar-roots',
                           style={'width': '30%', 'float': 'left', 'display': 'inline-block'}),
                 # --PLOT 3b:  IMPULSE RESPONSE FUNCTION----------------------------------------------------------------
                 dcc.Graph(id='plot-ma-roots',
                           style={'width': '30%', 'float': 'left', 'display': 'inline-block'}),
                 html.A(children='Randall Romero Aguilar', href='http://randall-romero.com', style={'textAlign': 'center', 'color': colors['text'],'marginBottom':60}),
             ]),
],
style={'backgroundColor': colors['background']})



@app.callback(
    [Output('title', 'children'),
     Output('plot-process', 'figure'),
     Output('plot-correlogram', 'figure'),
     Output('plot-partial-correlogram', 'figure'),
     Output('plot-irf', 'figure'),
     Output('plot-spectrum', 'figure'),
     Output('plot-ar-roots', 'figure'),
     Output('plot-ma-roots', 'figure'),
     Output('moments', 'children'),
     Output('moments', 'style'),
     Output('estimated', 'children'),
     ],
    [Input('execute', 'n_clicks')],
    [State('c', 'value'),
     State('AR', 'value'),
     State('MA', 'value'),
     State('vare', 'value'),
     State('periods', 'value'),
     State('lags', 'value'),
     State('horizon', 'value'),
     State('showestimates', 'value'),
     State('p', 'value'),
     State('q', 'value'),
     ])
def update_ARMA_parameters(n_clicks, c, phi, theta, sigma2, periods, lags, horizon, showestimates, p, q):
    phi = validate_lists_of_values(phi)
    theta = validate_lists_of_values(theta)
    Y = ARMA(c, phi, theta, sigma2, periods)
    Y.sample(int(periods) + 1)
    style = {'textAlign': 'center', 'color': colors['text'] if Y.isstationary else 'red'}
    Y.show_estimates = (showestimates == 'Yes')
    if Y.show_estimates:
        Y.estimate(int(p), int(q))

    return [
        str(Y),
        Y.plot_process(),
        Y.plot_correlogram(lags=int(lags)),
        Y.plot_partial_correlogram(lags=int(lags)), #FIXME
        Y.plot_irf(horizon=int(horizon)),
        Y.plot_spectral(),
        Y.plot_ar_roots(),
        Y.plot_ma_roots(),
        Y.print2moments(),
        style,
        Y.estimates['repr']
    ]



@app.callback(
    [Output('p,q', 'children'),
     Output('p,q', 'style')],
    [Input('showestimates', 'value')],
    [State('AR', 'value'),
     State('MA', 'value')])
def show_pq_options(showestimates, phi, theta):
    phi = validate_lists_of_values(phi)
    theta = validate_lists_of_values(theta)
    Y = ARMA(0, phi, theta, 1.0)
    p, q = Y.p, Y.q
    children = html.Tr([*app_parameter('p', 'p', 'text', p, '4'),
                        *app_parameter('q', 'q', 'text', q, '4')])
    style = {'display': 'none'} if (showestimates == 'No') else {}
    return children, style


def ARMA_demo():
    webbrowser.open('http://127.0.0.1:8050/')
    app.run_server(debug=False)


if __name__ == '__main__':
    ARMA_demo()

