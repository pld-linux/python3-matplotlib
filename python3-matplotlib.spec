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
Version:	3.10.7
Release:	1
License:	PSF
Group:		Libraries/Python
#Source0Download: https://github.com/matplotlib/matplotlib/releases
Source0:	https://github.com/matplotlib/matplotlib/archive/v%{version}/matplotlib-%{version}.tar.gz
# Source0-md5:	0e4136642c13c7784af76a72a6a0187e
Patch0:		relax-deps.patch
URL:		https://matplotlib.org/
# currently internal agg is used
#BuildRequires:	agg-devel
%{?with_system_freetype:BuildRequires:	freetype-devel >= 1:2.6.1}
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	meson >= 1.1.0
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.10
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.10
BuildRequires:	python3-installer
BuildRequires:	python3-numpy-devel >= 1:1.23
BuildRequires:	python3-meson-python >= 0.13.1
BuildRequires:	python3-pybind11 >= 2.13.4
BuildRequires:	python3-setuptools >= 1:64
BuildRequires:	python3-setuptools_scm >= 7
%{?with_system_qhull:BuildRequires:	qhull-devel >= 2015.2}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with tests}
BuildRequires:	ghostscript
BuildRequires:	gtk+3 >= 3.0
# /usr/bin/pdftops
BuildRequires:	poppler-progs
# or PyQt6>=6.1, PySide6, PySide2
BuildRequires:	python3-PyQt5
BuildRequires:	python3-contourpy >= 1.0.1
BuildRequires:	python3-cycler >= 0.10
BuildRequires:	python3-dateutil >= 2.7
BuildRequires:	python3-fonttools >= 4.22.0
BuildRequires:	python3-kiwisolver >= 1.3.1
BuildRequires:	python3-packaging >= 20.0
BuildRequires:	python3-pillow >= 8
# or cairocffi >= 0.8
BuildRequires:	python3-pycairo >= 1.11.0
BuildRequires:	python3-pygobject3 >= 3.0
BuildRequires:	python3-pyparsing >= 3
BuildRequires:	python3-pytest >= 3.6
BuildRequires:	python3-pytz
BuildRequires:	python3-tkinter >= 1:3.10
BuildRequires:	python3-tornado >= 5
#BuildRequires:	python3-wxPython >= 4
# /usr/bin/dvipng
BuildRequires:	texlive
BuildRequires:	texlive-xetex
# Font EU1/lmr/m/n/10=[lmroman10-regular]:mapping=tex-text at 10.0pt
#BuildRequires:	texlive-???
BuildRequires:	unzip
%endif
%if %{with doc}
BuildRequires:	python3-PyStemmer
BuildRequires:	python3-PyYAML
BuildRequires:	python3-colorspacious
BuildRequires:	python3-ipykernel
BuildRequires:	python3-ipython
BuildRequires:	python3-ipywidgets
BuildRequires:	python3-mpl-sphinx-theme >= 3.9.0
BuildRequires:	python3-numpydoc >= 1.0
BuildRequires:	python3-packaging >= 20
BuildRequires:	python3-pydata_sphinx_theme >= 0.15.0
BuildRequires:	python3-sphinx_copybutton
BuildRequires:	python3-sphinx_design
BuildRequires:	python3-sphinx_gallery >= 0.12.0
BuildRequires:	python3-sphinx_tags >= 0.4.0
BuildRequires:	python3-sphinxcontrib-svg2pdfconverter >= 1.1.0
BuildRequires:	python3-sphinxcontrib-video >= 0.2.1
BuildRequires:	sphinx-pdg >= 5.1.0
%endif
%{?with_system_freetype:Requires:	freetype >= 1:2.6.1}
Requires:	python3-modules >= 1:3.10
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
%patch -P0 -p1

%build

%py3_build_pyproject \
	-Csetup-args="-Dsystem-freetype=%{__true_false system_freetype}" \
	-Csetup-args="-Dsystem-qhull=%{__true_false system_qhull}"

%if %{with tests}
%__unzip -qo build-3/*.whl -d build-3/test-path
LIB="$(pwd)/build-3/test-path"
ln -sf $(readlink -f lib/matplotlib/tests/baseline_images) $LIB/matplotlib/tests/baseline_images
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$LIB \
%{__python3} -m pytest $LIB/matplotlib/tests -m 'not network'
%{__rm} $LIB/matplotlib/tests/baseline_images
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/matplotlib/tests
# matplotlib can use system fonts, so drop these copies
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/matplotlib/mpl-data/fonts/ttf/DejaVu*.ttf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md SECURITY.md LICENSE/LICENSE
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/*.pyi
%{py3_sitedir}/%{module}/__pycache__
%{py3_sitedir}/%{module}/py.typed
%attr(755,root,root) %{py3_sitedir}/%{module}/*.so
%{py3_sitedir}/%{module}/_api
%{py3_sitedir}/%{module}/axes
%dir %{py3_sitedir}/%{module}/backends
%{py3_sitedir}/%{module}/backends/*.py
%{py3_sitedir}/%{module}/backends/*.pyi
%{py3_sitedir}/%{module}/backends/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/backends/*.so
%dir %{py3_sitedir}/%{module}/backends/qt_editor
%{py3_sitedir}/%{module}/backends/qt_editor/*.py
%{py3_sitedir}/%{module}/backends/qt_editor/__pycache__
%{py3_sitedir}/%{module}/backends/web_backend
%{py3_sitedir}/%{module}/mpl-data
%{py3_sitedir}/%{module}/projections
%{py3_sitedir}/%{module}/sphinxext
%{py3_sitedir}/%{module}/style
%{py3_sitedir}/%{module}/testing
%{py3_sitedir}/%{module}/tri
%{py3_sitedir}/mpl_toolkits
%{py3_sitedir}/pylab.py
%{py3_sitedir}/__pycache__
%{py3_sitedir}/%{module}-%{version}.dist-info
