#
# Conditional build:
%bcond_with	tests	# unit tests [many failures as of 1.5.3]

# TODO:
# - use system fonts (mpl-data/fonts/ttf/{STIX,cm}*.ttf) and metrics (mpl-data/fonts/{afm,pdfcorefonts}/*.afm) in mpl-data dir?
# - make sure all dependencies that are available for Python3 are build for Python3
#   and included in BR when neccessary
%define		module	matplotlib
Summary:	Matlab(TM) style Python plotting package
Summary(pl.UTF-8):	Pakiet do rysowania w Pythonie podobny do Matlaba(TM)
Name:		python3-%{module}
Version:	3.2.1
Release:	2
License:	PSF
Group:		Libraries/Python
#Source0Download: https://github.com/matplotlib/matplotlib/releases
Source0:	https://github.com/matplotlib/matplotlib/archive/v%{version}/matplotlib-%{version}.tar.gz
# Source0-md5:	9186b1e9f1fc7d555f2abf64b35dea5b
Source1:	https://jqueryui.com/resources/download/jquery-ui-1.12.1.zip
# Source1-md5:	e0cfea21c9d1acd37fb58592f2c1f50d
Patch0:		%{name}-system-qhull.patch
URL:		https://matplotlib.org/
#BuildRequires:	agg-devel
BuildRequires:	freetype-devel >= 1:2.6.1
BuildRequires:	ghostscript
BuildRequires:	gtk+3 >= 3.0
BuildRequires:	libpng-devel >= 1.2
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
# /usr/bin/pdftops
BuildRequires:	poppler-progs
BuildRequires:	python3 >= 1:3.6
BuildRequires:	python3-2to3
BuildRequires:	python3-PyQt4
BuildRequires:	python3-PyQt5
BuildRequires:	python3-cycler >= 0.10
BuildRequires:	python3-dateutil >= 2.2
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-numpy-devel >= 1:1.7.1
# or cairocffi
BuildRequires:	python3-pycairo
BuildRequires:	python3-pygobject3-devel >= 3.0
BuildRequires:	python3-pyparsing >= 2.1.7
BuildRequires:	python3-pytz
BuildRequires:	python3-six >= 1.10
BuildRequires:	python3-setuptools
# for import pyqtconfig needed by qt detection.
BuildRequires:	python3-sip-devel
BuildRequires:	python3-tkinter
BuildRequires:	python3-tornado
#BuildRequires:	python3-wxPython >= 2.9
%if %{with tests}
BuildRequires:	python3-kiwisolver >= 1.0.1
BuildRequires:	python3-pytest >= 3.6
%endif
BuildRequires:	qhull-devel >= 2015.2
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
# /usr/bin/dvipng
BuildRequires:	texlive
BuildRequires:	tk-devel
Requires:	freetype >= 1:2.6.1
Requires:	python3-modules >= 1:3.6
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
%patch0 -p1

unzip -q %{SOURCE1} -d lib/matplotlib/backends/web_backend

%build
export CFLAGS="%{rpmcflags}"

%py3_build

%if %{with tests}
PYTHONPATH=$(readlink -f build-3/lib.*) \
%{__python3} tests.py --no-network
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
%{py3_sitedir}/%{module}/compat
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
