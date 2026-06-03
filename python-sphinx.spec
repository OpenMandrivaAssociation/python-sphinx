%define module sphinx

######################################################
# NOTE Disable these for bootstrapping nose and sphinx!!
######################################################
# NOTE Docs requires a number of packages which also require sphinx,
# NOTE which is a bit of a nightmare in of itself.
%bcond tests 0
%bcond doc 0

Name:		python-sphinx
Summary:	Python documentation generator
Version:	9.1.0
Release:	1
License:	BSD-2-Clause
Group:		Development/Python
URL:		https://sphinx-doc.org/
Source0:	https://github.com/sphinx-doc/sphinx/archive/v%{version}/%{name}-%{version}.tar.gz
Source100:	%{name}.rpmlintrc

BuildSystem:	python
BuildOption(prep):	-p1
BuildArch:	noarch

BuildRequires:	make
BuildRequires:	fdupes
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(flit-core)
BuildRequires:	python%{pyver}dist(wheel)
%if %{with doc}
BuildRequires:	python%{pyver}dist(alabaster)
BuildRequires:	python%{pyver}dist(babel)
BuildRequires:	python%{pyver}dist(docutils) >= 0.21
BuildRequires:	python%{pyver}dist(imagesize)
BuildRequires:	python%{pyver}dist(jinja2) >= 3.1
BuildRequires:	python%{pyver}dist(pygments)
BuildRequires:	python%{pyver}dist(requests)
BuildRequires:	python%{pyver}dist(roman-numerals)
BuildRequires:	python%{pyver}dist(snowballstemmer)
BuildRequires:	python%{pyver}dist(sphinxcontrib-applehelp)
BuildRequires:	python%{pyver}dist(sphinxcontrib-devhelp)
BuildRequires:	python%{pyver}dist(sphinxcontrib-htmlhelp)
BuildRequires:	python%{pyver}dist(sphinxcontrib-jsmath)
BuildRequires:	python%{pyver}dist(sphinxcontrib-qthelp)
BuildRequires:	python%{pyver}dist(sphinxcontrib-serializinghtml)
%endif
%if %{with tests}
BuildRequires:	python%{pyver}dist(cython)
BuildRequires:	python%{pyver}dist(defusedxml)
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(pytest-xdist)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(typing_extensions)
%endif
Obsoletes:	python2-sphinx < %{EVRD}
%rename python3-sphinx

%patchlist
#sphinx-9.0.4-fix-crash-generating-scons-docs.patch

%description
Sphinx is a tool that facilitates the creation of beautiful
documentation for Python projects from reStructuredText sources. It
was originally created to format the new documentation for Python, but
has since been cleaned up in the hope that it will be useful in many
other projects.

%if %{with doc}
%package doc
Summary:	Documentation for %{name}
Group:		Development/Python
License:	BSD-2-Clause
Requires:	%{name} = %{EVRD}

%description doc
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.

This package contains documentation in reST and HTML formats.
%endif

%prep -a
# Relax upper bounds on docutils
# related: https://github.com/sphinx-doc/sphinx/issues/14455#issuecomment-4573075675
sed -i 's:"docutils>=0.21,<0.23":"docutils>=0.21,<0.24":g' pyproject.toml

%if %{with doc}
%build -a
export PYTHONPATH="$PWD"
pushd doc
export SPHINXBUILD="%{__python} ../sphinx/cmd/build.py"
make html man SPHINXBUILD="$SPHINXBUILD"
rm -rf _build/html/.buildinfo
mv _build/html ..
%endif

%install -a
%if %{with doc}
pushd doc
# Deliver man pages
install -d %{buildroot}%{_mandir}/man1
mv _build/man/sphinx-*.1 %{buildroot}%{_mandir}/man1/
popd

# Deliver rst files
rm -rf doc/_build
sed -i 's|python ../sphinx-build.py|/usr/bin/sphinx-build|' doc/Makefile
mv doc reST

# Clean up non-python files
rm -rf %{buildroot}%{python_sitelib}/sphinx/locale/.DS_Store
rm -rf %{buildroot}%{python_sitelib}/sphinx/locale/.tx

# Install html and reST paths and fill contents
install -d %{buildroot}%{_docdir}/%name-doc/html
install -d %{buildroot}%{_docdir}/%name-doc/reST
cp -R html %{buildroot}%{_docdir}/%name-doc/
cp -R reST %{buildroot}%{_docdir}/%name-doc/

# run fdupes in the doc package buildroot
%fdupes %{buildroot}%{_docdir}/%{name}-doc
%endif

# Move language files to /usr/share;
# patch to support this incorporated in 0.6.6
pushd %{buildroot}%{python_sitelib}

for lang in `find sphinx/locale -maxdepth 1 -mindepth 1 -type d -not -path '*/__pycache__' -not -path '*/\.*' -printf "%f "`;
do
  install -d %{buildroot}%{_datadir}/sphinx/locale/$lang
  install -d %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES
  mv sphinx/locale/$lang/LC_MESSAGES/sphinx.js \
     %{buildroot}%{_datadir}/sphinx/locale/$lang/
  mv sphinx/locale/$lang/LC_MESSAGES/sphinx.mo \
    %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES/
  rm -rf sphinx/locale/$lang
done
popd

%find_lang sphinx

# Language files; Since these are javascript, it's not immediately obvious to
# find_lang that they need to be marked with a language.
(cd %{buildroot} && find . -name 'sphinx.js') | sed -e 's|^.||' | sed -e \
  's:\(.*/locale/\)\([^/_]\+\)\(.*\.js$\):%lang(\2) \1\2\3:' \
  >> sphinx.lang

%check
%if %{with tests}
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitelib}"
# All linkcheck tests and test_latex_images need internet to download items
# as does test_build_latex_doc needs internet to download pictures,
# test_signature_annotations doesn’t work
skiptests+="not linkcheck and not test_latex_images'
skiptests+=" and not test_signature_annotations and not test_copy_images"
skiptests+=" and not test_ext_imgconverter and not test_build_latex_doc"
pytest -rs -k "$skiptests"
%endif

%files -f sphinx.lang
%doc README.rst
%{_bindir}/sphinx-*
%{python_sitelib}/%{module}
%{python_sitelib}/%{module}-%{version}.dist-info
%dir %{_datadir}/sphinx/
%dir %{_datadir}/sphinx/locale
%dir %{_datadir}/sphinx/locale/*
%if %{with doc}
%doc %{_mandir}/man1/*
%endif

%if %{with doc}
%files doc
%doc %{_docdir}/%{name}-doc/html
%doc %{_docdir}/%{name}-doc/reST
%endif
