%define tarname	Sphinx

# disable these for bootstrapping nose and sphinx
%bcond_with tests
%bcond_without doc
%bcond_without python2

Summary:	Python documentation generator

Name:		python-sphinx
Version:	1.2.3
Release:	3
Source0:	http://pypi.python.org/packages/source/S/Sphinx/Sphinx-%{version}.tar.gz
Patch0:	        Sphinx-1.2.2-mantarget.patch
Patch1:         Sphinx-1.2.2-babel-option.patch
Patch2:		Sphinx-1.2.2-python3.patch
License:	BSD
Group:		Development/Python
Url:		http://sphinx.pocoo.org/
BuildArch:	noarch
Requires:	python-pkg-resources
Requires:	python-docutils
Requires:	python-jinja2
Requires:	python-pygments
BuildRequires:	python-setuptools
%if %{with doc}
BuildRequires:	python-docutils >= 0.7
BuildRequires:	python-jinja2 >= 2.3
%endif
%if %{with tests}
BuildRequires:	python-nose
BuildRequires:	python-pygments
BuildRequires:  python-jinja2
%endif
BuildRequires:	pkgconfig(python3)
BuildRequires:	python3-distribute
%rename python3-sphinx

%description
Sphinx is a tool that facilitates the creation of beautiful
documentation for Python projects from reStructuredText sources. It
was originally created to format the new documentation for Python, but
has since been cleaned up in the hope that it will be useful in many
other projects.

%if %{with python2}
%package -n python2-sphinx
Summary:	Python documentation generator for Python 2.x
Group:		Development/Python
Requires:	python2-docutils >= 0.7
Requires:	python2-pygments >= 1.2
Requires:	python2-jinja2 >= 2.3
BuildRequires:	pkgconfig(python2)
BuildRequires:	python2-nose
BuildRequires:	python2-pygments
BuildRequires:  python2-jinja2
BuildRequires:	python2-setuptools

%description -n python2-sphinx
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.
%endif

%if %{with doc}
%package doc
Summary:	Documentation for %{name}

Group:		Development/Python
License:	BSD
Requires:	%{name} = %{version}-%{release}

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
%setup -qc
tar xzf %{SOURCE0}
cd %{tarname}-%{version}
%patch0 -p1 -b .mantarget
%patch1 -p1 -b .babel
sed '1d' -i sphinx/pycode/pgen2/token.py
cd ..

mv %{tarname}-%{version} python3

%if %{with python2}
cp -r python3 python2
%endif

cd python3
# Modifications needed only for python 3.x build
find . -name "*.py" |xargs 2to3 -w
%patch2 -p1 -b .py3~

%build
%if %{with python2}
cd python2
python2 setup.py build
cd ..
%endif

cd python3
python setup.py build
cd ..

%if %{with doc}
cd python3/doc
make html man
rm -rf _build/html/.buildinfo
mv _build/html ..
cd ../..
%endif


%install
%if %{with python2}
cd python2
python2 setup.py install --skip-build --root %{buildroot}
for f in %{buildroot}%{_bindir}/sphinx-*;
do
 mv $f $f-%{python2_version}
done
ln -s %{_bindir}/sphinx-build-%{python2_version} %{buildroot}%{_bindir}/sphinx-build2
cd ..
%endif

cd python3
python setup.py install --skip-build --root=%{buildroot} 

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
cd ..

# Move language files to /usr/share;
# patch to support this incorporated in 0.6.6
pushd %{buildroot}%{py_puresitedir}

for lang in `find sphinx/locale -maxdepth 1 -mindepth 1 -type d -not -path '*/\.*' -printf "%f "`;
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
%if %{with python2}
cd python2/tests
python2 run.py
cd ../..
%endif
cd python3
make test
cd ..
%endif

%files -f sphinx.lang
%doc python3/AUTHORS python3/CHANGES python3/EXAMPLES python3/LICENSE
%{_bindir}/sphinx-*
%{py_puresitedir}/*
%dir %{_datadir}/sphinx/
%dir %{_datadir}/sphinx/locale
%dir %{_datadir}/sphinx/locale/*
%{_mandir}/man1/*
%if %{with python2}
%exclude %{_bindir}/sphinx-*-%{python2_version}
%exclude %{_bindir}/sphinx-build2
%exclude %{py2_puresitedir}/*
%endif

%if %{with python2}
%files -n python2-sphinx
%doc python2/AUTHORS python2/CHANGES python2/EXAMPLES python2/LICENSE
%{_bindir}/sphinx-*-%{python2_version}
%{_bindir}/sphinx-build2
%{py2_puresitedir}/*
%dir %{_datadir}/sphinx/
%dir %{_datadir}/sphinx/locale
%dir %{_datadir}/sphinx/locale/*
%endif

%if %{with doc}
%files doc
%doc python3/html python3/reST
%endif
