%define tarname	Sphinx
%define name	python-sphinx
%define version	1.1.3
%define release	1

# disable these for bootstrapping nose and sphinx
%define enable_tests 1
%define enable_doc 1

Summary:	Python documentation generator
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://pypi.python.org/packages/source/S/%{tarname}/%{tarname}-%{version}.tar.gz
Patch0:         Sphinx-1.1.3-sagemath.patch
License:	BSD
Group:		Development/Python
Url:		http://sphinx.pocoo.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:	noarch
Requires:	python-pkg-resources
Requires:	python-docutils >= 0.7
Requires:	python-pygments >= 1.2
Requires:	python-jinja2 >= 2.3
BuildRequires:	python-setuptools
Requires:	python-pygments >= 1.2
%if %enable_doc
BuildRequires:	python-docutils >= 0.7
BuildRequires:	python-jinja2 >= 2.3
%endif
%if %enable_tests
BuildRequires:	python-nose
%endif
%py_requires -d

%description
Sphinx is a tool that facilitates the creation of beautiful
documentation for Python projects from reStructuredText sources. It
was originally created to format the new documentation for Python, but
has since been cleaned up in the hope that it will be useful in many
other projects.

%prep
%setup -q -n %{tarname}-%{version}
%patch0 -p1

%install
%__rm -rf %{buildroot}
PYTHONDONTWRITEBYTECODE= %__python setup.py install --root=%{buildroot}
%if %enable_doc
%__make -C doc html
%endif
%clean
%__rm -rf %{buildroot}

%check
%if %enable_tests
pushd tests
%__python run.py
popd
%endif

%files
%defattr(-,root,root)
%doc AUTHORS CHANGES LICENSE TODO 
%if %enable_doc
%doc doc/_build/html/
%endif
%_bindir/sphinx*
%py_sitedir/sphinx/
%py_sitedir/Sphinx-*egg-info/


%changelog
* Wed Apr 18 2012 Lev Givon <lev@mandriva.org> 1.1.3-1
+ Revision: 791777
- Update to 1.1.3.

* Sat Nov 05 2011 Paulo Andrade <pcpa@mandriva.com.br> 1.1.2-2
+ Revision: 720231
- Update sagemath patch to properly generate sagemath 4.7.2 documentation.

* Wed Nov 02 2011 Lev Givon <lev@mandriva.org> 1.1.2-1
+ Revision: 712226
- Update to 1.1.2.

* Tue Nov 01 2011 Lev Givon <lev@mandriva.org> 1.1.1-1
+ Revision: 709342
- Update to 1.1.1.

* Tue Oct 11 2011 Lev Givon <lev@mandriva.org> 1.1-1
+ Revision: 704139
- Update to 1.1.

* Thu Jun 09 2011 Antoine Ginies <aginies@mandriva.com> 1.0.7-3
+ Revision: 683472
- rebuild

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.7-2
+ Revision: 668036
- mass rebuild

* Tue Jan 18 2011 Lev Givon <lev@mandriva.org> 1.0.7-1
+ Revision: 631630
- Update to 1.0.7.

* Fri Nov 12 2010 Lev Givon <lev@mandriva.org> 1.0.5-1mdv2011.0
+ Revision: 596694
- Update to 1.0.5.

* Sat Oct 30 2010 Michael Scherer <misc@mandriva.org> 1.0.4-3mdv2011.0
+ Revision: 590417
- reenable test and documentation, now that requirement are here

* Sat Oct 30 2010 Michael Scherer <misc@mandriva.org> 1.0.4-2mdv2011.0
+ Revision: 590369
- also fix the documentation generation ( bootstraping problem, since jinja2 requires sphinx too )
- disable test ( as nose requires sphinx, and sphinx requires nose, they cannot be upgraded to 2.7 )
- rebuild for python 2.7

* Fri Sep 17 2010 Lev Givon <lev@mandriva.org> 1.0.4-1mdv2011.0
+ Revision: 579194
- Update to 1.0.4.

* Wed Sep 15 2010 Lev Givon <lev@mandriva.org> 1.0.3-1mdv2011.0
+ Revision: 578780
- Update to 1.0.3.

* Tue Jul 27 2010 Lev Givon <lev@mandriva.org> 0.6.7-1mdv2011.0
+ Revision: 562106
- Update to 0.6.7.
- Update to 0.6.6.

* Thu Mar 11 2010 Lev Givon <lev@mandriva.org> 0.6.5-1mdv2010.1
+ Revision: 518262
- Update to 0.6.5.

* Wed Jan 13 2010 Lev Givon <lev@mandriva.org> 0.6.4-1mdv2010.1
+ Revision: 491048
- Update to 0.6.4.

* Tue Sep 08 2009 Lev Givon <lev@mandriva.org> 0.6.3-1mdv2010.0
+ Revision: 433689
- Update to 0.6.3.
  Build docs as html.

* Wed Aug 05 2009 Paulo Andrade <pcpa@mandriva.com.br> 0.6.2-2mdv2010.0
+ Revision: 409716
- Add sagemath patch to python-sphinx.

* Wed Jun 17 2009 Lev Givon <lev@mandriva.org> 0.6.2-1mdv2010.0
+ Revision: 386763
- Update to 0.6.2.

* Fri May 22 2009 Lev Givon <lev@mandriva.org> 0.6.1-1mdv2010.0
+ Revision: 378621
- Update to 0.6.1.

* Mon May 04 2009 Lev Givon <lev@mandriva.org> 0.5.2-2mdv2010.0
+ Revision: 371821
- Fix requirements.

* Tue Mar 24 2009 Lev Givon <lev@mandriva.org> 0.5.2-1mdv2010.0
+ Revision: 360951
- Update to 0.5.2.
  Change python-setuptools install requirement to python-pkg-resources.

* Sun Jan 04 2009 Jérôme Soyer <saispo@mandriva.org> 0.5.1-1mdv2009.1
+ Revision: 324276
- New upstream release

* Sun Dec 28 2008 Funda Wang <fwang@mandriva.org> 0.5-2mdv2009.1
+ Revision: 320265
- rebuild for new python

* Tue Dec 02 2008 Lev Givon <lev@mandriva.org> 0.5-1mdv2009.1
+ Revision: 308946
- Update to 0.5.

* Sun Oct 19 2008 Lev Givon <lev@mandriva.org> 0.4.3-1mdv2009.1
+ Revision: 295422
- Update to 0.4.3.

* Wed Aug 06 2008 Lev Givon <lev@mandriva.org> 0.4.2-2mdv2009.0
+ Revision: 264333
- Add setuptools as an install requirement
  (pkg_resources needed by sphinx-build).

* Wed Aug 06 2008 Lev Givon <lev@mandriva.org> 0.4.2-1mdv2009.0
+ Revision: 264111
- Update to 0.4.2.

* Fri Jul 11 2008 Lev Givon <lev@mandriva.org> 0.4.1-1mdv2009.0
+ Revision: 233844
- Update to 0.4.1.

* Mon Jun 23 2008 Lev Givon <lev@mandriva.org> 0.4-1mdv2009.0
+ Revision: 228282
- Update to 0.4.

* Fri May 30 2008 Lev Givon <lev@mandriva.org> 0.3-1mdv2009.0
+ Revision: 213482
- import python-sphinx


* Thu May 29 2008 Lev Givon <lev@mandriva.org> 0.3-1mdv2008.1
- Package for Mandriva.
