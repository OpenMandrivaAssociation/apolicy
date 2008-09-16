Summary:	ACL Policy Daemon for Postfix
Name:		apolicy
Version:	0.73
Release:	%mkrel 1
License:	GPL
Group:		System/Servers
Source:		http://download.gna.org/apolicy/%{name}-%{version}.tar.gz
Source1:	http://download.gna.org/apolicy/%{name}-%{version}.tar.gz.sig
Source2:	http://www.apolicy.org/gpg/miguelfilho.gpg
Source3:	apolicy-readme.mdv
Patch:		apolicy-mdv.patch
URL:		http://www.apolicy.org/
Buildarch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot/
BuildRequires:	python-devel >= 2.3
Requires:	python-pydns >= 2.3
Requires:	python-pyspf >= 2.0
Requires:	python-twisted-core >= 2.4
Requires:	python-IPy >= 0.53
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
rm -rf %{buildroot}
python setup.py install --skip-build --root %{buildroot}
/bin/mkdir -p %{buildroot}/var/cache/%{name}
/bin/mkdir -p %{buildroot}%{_initrddir}
install -c %{name}.init %{buildroot}%{_initrddir}/%{name}

%clean
rm -rf %{buildroot}

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

