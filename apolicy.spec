Summary:	ACL Policy Daemon for Postfix
Name:		apolicy
Version:	0.73
Release:	5
License:	GPL
Group:		System/Servers
Source:		http://download.gna.org/apolicy/%{name}-%{version}.tar.gz
Source1:	http://download.gna.org/apolicy/%{name}-%{version}.tar.gz.sig
Source2:	http://www.apolicy.org/gpg/miguelfilho.gpg
Source3:	apolicy-readme.mdv
Patch0:		apolicy-mdv.patch
URL:		http://www.apolicy.org/
Buildarch:	noarch
%py_requires -d
Requires:	python-pydns >= 2.3
Requires:	python-pyspf >= 2.0
Requires:	python-twisted-core >= 2.4
Requires:	python-ipy
Requires:	python-memcached
Requires(pre):	rpm-helper

%description
ACL Policy Daemon communicates with the Postfix MTA using the Policy Delegation
Protocol, implementing an ACL (Access Control List) system.
Key features:
greylisting with flexible storage using memory for fast responses or disk for
high persistence, SPF validation, control of messages by day/time, variable
message size limits per domain or email, multiple RBL checking, and various
ACLs available to use and combine.
The configuration is simple and intuitive.

Please check README.MDV file for post-installation instructions

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .mdv
cp %{SOURCE3} README.MDV

%build
perl -spi -e 's/\r$//' docs/*.txt
python setup.py build

%install
python setup.py install --skip-build --root %{buildroot}
/bin/mkdir -p %{buildroot}/var/cache/%{name}
/bin/mkdir -p %{buildroot}%{_initrddir}
install -c %{name}.init %{buildroot}%{_initrddir}/%{name}

%files
%defattr(-,root,root,755)
%doc README.MDV
%doc CONTRIBUTORS.TXT  README.TXT LICENSE.TXT docs/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_initrddir}/%{name}
%{py_sitedir}/%{name}
%{py_sitedir}/%{name}-%{version}-py%{py_ver}.egg-info
%attr(0700,nobody,nogroup) /var/cache/%{name}

%post
%_post_service %{name}

%preun
%_preun_service %{name}



%changelog
* Sun Oct 31 2010 Funda Wang <fwang@mandriva.org> 0.73-4mdv2011.0
+ Revision: 590785
- rebuild for py2.7

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 0.73-3mdv2010.0
+ Revision: 436655
- rebuild

* Sun Jan 04 2009 Funda Wang <fwang@mandriva.org> 0.73-2mdv2009.1
+ Revision: 324150
- rebuild

* Tue Sep 16 2008 Luca Berra <bluca@mandriva.org> 0.73-1mdv2009.0
+ Revision: 285254
- import apolicy


* Mon Sep 08 2008 Luca Berra <bluca@mandriva.org> 0.73-1mdv2009.0
- Initial mandriva package
