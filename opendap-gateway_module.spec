# NOTE: for versions >= 1.1.6 see bes.spec
#
# Conditional build:
%bcond_with	tests	# make check (requires BES server)
#
Summary:	Gateway module for the OPeNDAP data server
Summary(pl.UTF-8):	Moduł bramki dla serwera danych OPeNDAP
Name:		opendap-gateway_module
Version:	1.1.2
Release:	2
License:	LGPL v2.1+
Group:		Daemons
Source0:	http://www.opendap.org/pub/source/gateway_module-%{version}.tar.gz
# Source0-md5:	b2cf29accb7d0b35a90bbd1773837ba1
Patch0:		%{name}-includes.patch
Patch1:		%{name}-link.patch
URL:		http://opendap.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.10
%{?with_tests:BuildRequires:	bes >= 3.13.0}
BuildRequires:	bes-devel >= 3.13.0
BuildRequires:	bes-devel < 3.14
BuildRequires:	curl-devel
BuildRequires:	libdap-devel >= 3.13.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
Requires:	bes >= 3.13.0
Requires:	libdap >= 3.13.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the Gateway module for the OPeNDAP data server. It allows a
remote URL to be passed as a container to the BES, have that remote
URL accessed, and served locally.

%description -l pl.UTF-8
Ten pakiet zawiera moduł bramki (Gateway) dla serwera danych OPeNDAP.
Pozwala na przekazanie zdalnego URL-a jako kontenera do BES, który
odwołuje się do tego zdalnego URL-a i serwuje go lokalnie.

%prep
%setup -q -n gateway_module-%{version}
%patch0 -p1
%patch1 -p1

%build
# rebuild autotools for -as-needed to work
%{__libtoolize}
%{__aclocal} -I conf
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/bes/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYRIGHT ChangeLog NEWS README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bes/modules/gateway.conf
%attr(755,root,root) %{_libdir}/bes/libgateway_module.so
