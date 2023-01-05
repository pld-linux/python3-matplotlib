#
# Conditional build:
%bcond_with	doc		# Sphinx documentation
%bcond_with	tests		# unit tests [many failures as of 3.5.1, esp. with system freetype]
%bcond_without	system_freetype	# system freetype library
%bcond_without	system_qhull	# system qhull library

# TODO:
# - finish doc
# - use system fonts (mpl-data/fonts/ttf/{STIX,cm}*.ttf) and metrics (mpl-data/fonts/{afm,pdfcorefonts}/*.afm) in mpl-data dir?
# - make sure all dependencies that are available for Python3 are build for Python3
#   and included in BR when neccessary
%define		module	matplotlib
Summary:	Matlab(TM) style Python plotting package
Summary(pl.UTF-8):	Pakiet do rysowania w Pythonie podobny do Matlaba(TM)
Name:		python3-%{module}
Version:	3.5.3
Release:	1
License:	PSF
Group:		Libraries/Python
#Source0Download: https://github.com/matplotlib/matplotlib/releases
Source0:	https://github.com/matplotlib/matplotlib/archive/v%{version}/matplotlib-%{version}.tar.gz
# Source0-md5:	3e865ad2653e5c9ba068823075bb2b44
URL:		https://matplotlib.org/
# currently internal agg is used
#BuildRequires:	agg-devel
%{?with_system_freetype:BuildRequires:	freetype-devel >= 1:2.6.1}
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.7
BuildRequires:	python3-certifi >= 2020.6.20
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-numpy-devel >= 1:1.17
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm >= 4
BuildRequires:	python3-setuptools_scm < 7
BuildRequires:	python3-setuptools_scm_git_archive
%{?with_system_qhull:BuildRequires:	qhull-devel >= 2015.2}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with tests}
BuildRequires:	ghostscript
BuildRequires:	gtk+3 >= 3.0
# /usr/bin/pdftops
BuildRequires:	poppler-progs
# or PyQt6>=6.1, PySide6, PySide2
BuildRequires:	python3-PyQt5
BuildRequires:	python3-cycler >= 0.10
BuildRequires:	python3-dateutil >= 2.7
BuildRequires:	python3-fonttools >= 4.22.0
BuildRequires:	python3-kiwisolver >= 1.0.1
BuildRequires:	python3-packaging >= 20.0
BuildRequires:	python3-pillow >= 6.2.0
# or cairocffi >= 0.8
BuildRequires:	python3-pycairo >= 1.11.0
BuildRequires:	python3-pygobject3 >= 3.0
BuildRequires:	python3-pyparsing >= 2.2.1
BuildRequires:	python3-pytest >= 3.6
BuildRequires:	python3-pytz
BuildRequires:	python3-tkinter >= 1:3.7
BuildRequires:	python3-tornado >= 5
#BuildRequires:	python3-wxPython >= 4
# /usr/bin/dvipng
BuildRequires:	texlive
BuildRequires:	texlive-xetex
# Font EU1/lmr/m/n/10=[lmroman10-regular]:mapping=tex-text at 10.0pt
#BuildRequires:	texlive-???
%endif
%if %{with doc}
BuildRequires:	python3-colorspacious
BuildRequires:	python3-ipython
BuildRequires:	python3-ipywidgets
BuildRequires:	python3-mpl-sphinx-theme
BuildRequires:	python3-numpydoc >= 0.8
BuildRequires:	python3-packaging >= 20
BuildRequires:	python3-scipy
BuildRequires:	python3-sphinx_copybutton
BuildRequires:	python3-sphinx_gallery >= 0.10
BuildRequires:	python3-sphinx_panels
BuildRequires:	python3-sphinxcontrib-svg2pdfconverter >= 1.1.0
BuildRequires:	sphinx-pdg >= 2.0.1
%endif
%{?with_system_freetype:Requires:	freetype >= 1:2.6.1}
Requires:	python3-modules >= 1:3.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
matplotlib strives to produce publication quality 2D graphics using
matlab plotting for inspiration. Although the main lib is object
oriented, there is a functional interface "pylab" for people coming
from Matlab.

%description -l pl.UTF-8
matplotlib usiłuje tworzyć grafikę 2D o jakości publikacji przy użyciu
wykresów matlaba jako inspiracji. Chociaż główna biblioteka jest
zorientowana obiektowo, jest interfejs funkcyjny "pylab" dla ludzi
przechodzących z Matlaba.

%prep
%setup -q -n %{module}-%{version}

cat >mplsetup.cfg <<EOF
[libs]
%if %{with system_freetype}
system_freetype = True
%endif
%if %{with system_qhull}
system_qhull = True
%endif
EOF

%build
export CFLAGS="%{rpmcflags}"

%py3_build

%if %{with tests}
LIB=$(readlink -f build-3/lib.*)
ln -sf $(readlink -f lib/matplotlib/tests/baseline_images) $LIB/matplotlib/tests/baseline_images
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$LIB \
%{__python3} -m pytest $LIB/matplotlib/tests -m 'not network'
%{__rm} $LIB/matplotlib/tests/baseline_images
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/matplotlib/tests
# matplotlib can use system fonts, so drop these copies
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/matplotlib/mpl-data/fonts/ttf/DejaVu*.ttf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst LICENSE/LICENSE
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/*.so
%{py3_sitedir}/%{module}/_api
%{py3_sitedir}/%{module}/axes
%dir %{py3_sitedir}/%{module}/backends
%{py3_sitedir}/%{module}/backends/*.py
%{py3_sitedir}/%{module}/backends/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/backends/*.so
%dir %{py3_sitedir}/%{module}/backends/qt_editor
%{py3_sitedir}/%{module}/backends/qt_editor/*.py
%{py3_sitedir}/%{module}/backends/qt_editor/__pycache__
%{py3_sitedir}/%{module}/backends/web_backend
%{py3_sitedir}/%{module}/cbook
%{py3_sitedir}/%{module}/mpl-data
%{py3_sitedir}/%{module}/projections
%{py3_sitedir}/%{module}/sphinxext
%{py3_sitedir}/%{module}/style
%{py3_sitedir}/%{module}/testing
%{py3_sitedir}/%{module}/tri
%{py3_sitedir}/mpl_toolkits
%{py3_sitedir}/pylab.py
%{py3_sitedir}/__pycache__
%{py3_sitedir}/%{module}-%{version}-py*.egg-info
%{py3_sitedir}/%{module}-%{version}-py*-nspkg.pth
