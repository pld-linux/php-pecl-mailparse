# TODO
# - doesn't build
%define		_modname	mailparse
%define		_status		beta
Summary:	Email message manipulation
Summary(pl):	Obrabianie wiadomości E-mail
Name:		php-pecl-%{_modname}
Version:	0.9.2
Release:	0.3
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	73478cc638522aefb7315cc1976f76d4
URL:		http://pecl.php.net/package/mailparse/
BuildRequires:	php-devel >= 4:5.2.0-7.2
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mailparse is an extension for parsing and working with email messages.
It can deal with rfc822 and rfc2045 (MIME) compliant messages.

In PECL status of this package is: %{_status}.

%description -l pl
Mailparse to rozszerzenie do analizy i pracy z wiadomościami poczty
elektronicznej. Radzi sobie z wiadomościami zgodnymi z RFC822 oraz
RFC2024 (MIME).

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure \
	--with-%{_modname}=%{_prefix}/X11R6/include/X11/

%{__make} CPPFLAGS="-DHAVE_CONFIG_H -I%{_prefix}/X11R6/include/X11"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install %{_smodname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
