%define tarname sphinx

# disable these for bootstrapping nose and sphinx
%bcond_with tests
%bcond_with doc

%define __noautoreq 'pythonegg\\(typing\\)'
%define upstreamver %(echo %{version} |sed -e 's,[~+],,')

Summary:	Python documentation generator
Name:		python-sphinx
Version:	8.2.3
Release:	2
Source0:	https://github.com/sphinx-doc/sphinx/archive/v%{upstreamver}/%{tarname}-%{version}.tar.gz
Source1000:	%{name}.rpmlintrc
License:	BSD
Group:		Development/Python
Url:		https://sphinx-doc.org/
BuildArch:	noarch
Requires:	python-pkg-resources
Requires:	python-docutils
Requires:	python-jinja2
Requires:	python-pygments
Requires:	python-sphinxcontrib-websupport
Requires:	python-imagesize
BuildRequires:	python-pip
BuildRequires:	python-wheel
%if %{with doc}
BuildRequires:	python-docutils >= 0.7
BuildRequires:	python-jinja2 >= 2.3
%endif
%if %{with tests}
BuildRequires:	python-nose
BuildRequires:	python-pygments
BuildRequires:  python-jinja2
%endif
BuildRequires:	pkgconfig(python)
BuildRequires:	python-setuptools
Obsoletes:	python2-sphinx < %{EVRD}
%rename python3-sphinx

%patchlist
sphinx-8.2.3-compile.patch
https://github.com/sphinx-doc/sphinx/pull/13786.patch

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
License:	BSD
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

%prep
%autosetup -n %{tarname}-%{upstreamver} -p1

%build
%py_build

%if %{with doc}
cd doc
make html man
rm -rf _build/html/.buildinfo
mv _build/html ..
%endif

%install
%py_install

%if %{with doc}
cd doc
# Deliver man pages
install -d %{buildroot}%{_mandir}/man1
mv _build/man/sphinx-*.1 %{buildroot}%{_mandir}/man1/
cd ..

# Deliver rst files
rm -rf doc/_build
sed -i 's|python ../sphinx-build.py|/usr/bin/sphinx-build|' doc/Makefile
mv doc reST
%endif

# Move language files to /usr/share;
# patch to support this incorporated in 0.6.6
pushd %{buildroot}%{py_puresitedir}

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
make test
%endif

%files -f sphinx.lang
%{_bindir}/sphinx-*
%{py_puresitedir}/*
%dir %{_datadir}/sphinx/
%dir %{_datadir}/sphinx/locale
%dir %{_datadir}/sphinx/locale/*
%if %{with doc}
%doc %{_mandir}/man1/*
%endif

%if %{with doc}
%files doc
%doc html reST
%endif
