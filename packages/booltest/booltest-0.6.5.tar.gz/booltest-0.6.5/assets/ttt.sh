export CFHOME="/storage/brno3-cerot/home/${LOGNAME}"

module add gcc-5.3.0
module add cmake-3.6.1
module add mpc-1.0.3
module add gmp-6.1.2
module add mpfr-3.1.4

export PYENV_ROOT="${CFHOME}/.pyenv"
export PATH="${PYENV_ROOT}/bin:${PATH}"

git clone https://github.com/pyenv/pyenv.git "${CFHOME}/.pyenv"
eval "$(pyenv init -)"
pyenv install 2.7.14
pyenv install 3.6.4
pyenv local 3.6.4





export HOMEDIR="/storage/brno3-cerit/home/${LOGNAME}"
export PYENV_ROOT="${HOMEDIR}/.pyenv"
export PATH="${PYENV_ROOT}/bin:${PATH}"
cd $HOMEDIR

module add gcc-5.3.0
module add cmake-3.6.1
module add mpc-1.0.3
module add gmp-6.1.2
module add mpfr-3.1.4

eval "$(pyenv init -)"
pyenv local 3.6.4

pyenv install 2.7.14
pyenv install 3.6.4




