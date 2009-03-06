# TODO:
# - support for libdclassify
# - oracle driver
# - messages from default install of cron with mysql driver Memory fault
#
# Conditional build:
%bcond_without	mysql	# disable MySQL storage driver
%bcond_without	pgsql	# disable PostgreSQL storage driver
%bcond_without	sqlite	# disable SQLite3 storage driver
%bcond_with	mysql40 # use with mysql 4.0
#
%include	/usr/lib/rpm/macros.perl
Summary:	A library and Mail Delivery Agent for Bayesian spam filtering
Summary(pl.UTF-8):	Biblioteka i MDA do bayesowskiego filtrowania spamu
Name:		dspam
Version:	3.8.0
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	http://dspam.nuclearelephant.com/sources/%{name}-%{version}.tar.gz
# Source0-md5:	056b8c8b3ad9415a52c01b22ff1e64cf
Patch0:		%{name}-webui.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-speedup.patch
Patch3:		%{name}-autotools.patch
Source1:	%{name}.init
Source2:	%{name}-apache.conf
URL:		http://dspam.nuclearelephant.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	clamav-devel
BuildRequires:	libtool
%{?with_mysql:BuildRequires:	mysql-devel}
BuildRequires:	openldap-devel >= 2.4.6
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
%{?with_sqlite:BuildRequires:	sqlite3-devel}
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{version}-%{release}
Requires:	%{name}-driver = %{version}-%{release}
Requires:	rc-scripts
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}

%description
DSPAM (as in De-Spam) is an open-source project to create a new kind
of anti-spam mechanism, and is currently effective as both a
server-side agent for UNIX email servers and a developer's library for
mail clients, other anti-spam tools, and similar projects requiring
drop-in spam filtering.

The DSPAM agent masquerades as the email server's local delivery agent
and filters/learns spams using an advanced Bayesian statistical
approach (based on Bayes's theorem of combined probabilities) which
provides an administratively maintenance-free, easy-learning Anti-Spam
service custom tailored to each individual user's behavior. Advanced
because on top of standard Bayesian filtering is also incorporated the
use of Chained Tokens, de-obfuscation, and other enhancements. DSPAM
works great with Sendmail and Exim, and should work well with any
other MTA that supports an external local delivery agent (postfix,
qmail, etc.)

%description -l pl.UTF-8
DSPAM (czyli De-Spam) to projekt o otwartych źródłach mający na celu
stworzenie nowego rodzaju mechanizmu antyspamowego. Aktualnie jest
efektywny zarówno jako działający po stronie serwera agent dla
uniksowych serwerów pocztowych jak i biblioteka dla programistów
klientów pocztowych, innych narzędzi antyspamowych i innych projektów
wymagających filtrowania spamu w locie.

Agent DSPAM zachowuje się jak lokalny agent dostarczania poczty (MDA)
i filtruje/uczy się spamu przy użyciu zaawansowanego bayesowskiego
przybliżenia statystycznego (opartego na twierdzeniu Bayesa o
połączonych prawdopodobieństwach), dając nie wymagającą obsługi
administracyjnej, łatwo uczącą się usługę antyspamową dostosowaną do
zachowania każdego użytkownika. Metoda jest zaawansowana ponieważ na
podstawie standardowego filtrowania bayesowskiego wprowadzono użycie
tokenów łańcuchowych, eliminowanie ukrywanie i inne rozszerzenia.
DSPAM działa wspaniale z Sendmailem i Eximem, powinien działać dobrze
z każdym innym MTA obsługującym zewnętrznego agenta MDA (postfiksem,
qmailem itd.).

%package client
Summary:	dspam client
Summary(pl.UTF-8):	Klient dspam
Group:		Applications/Mail
Requires:	%{name}-common

%description client
dspam client.

%description client -l pl.UTF-8
Klient dspam.

%package common
Summary:	Common files for dspam packages
Summary(pl.UTF-8):	Wspólne pliki dla pakietów z dspamem
Group:		Applications/Mail

%description common
Common files for dspam and dspam-client packages.

%description client -l pl.UTF-8
Wspólne pliki dla pakietów dspam i dspam-client.

%package libs
Summary:	A library for Bayesian spam filtering
Summary(pl.UTF-8):	Biblioteka do bayesowskiego filtrowania spamu
Group:		Libraries
Obsoletes:	dspam-driver-db

%description libs
DSPAM (as in De-Spam) is an open-source project to create a new kind
of anti-spam mechanism, and is currently effective as both a
server-side agent for UNIX email servers and a developer's library for
mail clients, other anti-spam tools, and similar projects requiring
drop-in spam filtering.

This package contains the library.

%description libs -l pl.UTF-8
DSPAM (czyli De-Spam) to projekt o otwartych źródłach mający na celu
stworzenie nowego rodzaju mechanizmu antyspamowego. Aktualnie jest
efektywny zarówno jako działający po stronie serwera agent dla
uniksowych serwerów pocztowych jak i biblioteka dla programistów
klientów pocztowych, innych narzędzi antyspamowych i innych projektów
wymagających filtrowania spamu w locie.

Ten pakiet zawiera wspomnianą bibliotekę.

%package devel
Summary:	Header files for the DSPAM library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki DSPAM
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
DSPAM has had its core engine moved into a separate library, libdspam.
This library can be used by developers to provide 'drop-in' spam
filtering for their mail client applications, other anti-spam tools,
or similar projects.

%description devel -l pl.UTF-8
Główny silnik DSPAM został przeniesiony do oddzielnej biblioteki
libdspam, która może być używana przez programistów do zapewnienia
filtrowania spamu w locie dla aplikacji klientów pocztowych, innych
narzędzi antyspamowych i podobnych projektów.

%package static
Summary:	Static DSPAM library
Summary(pl.UTF-8):	Statyczna biblioteka DSPAM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static DSPAM library.

%description static -l pl.UTF-8
Statyczna biblioteka DSPAM.

%package driver-hash
Summary:	HASH driver for DSPAM
Summary(pl.UTF-8):	Sterownik HASH dla DSPAM-a
Group:		Libraries
Requires(post):	sed >= 4.0
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-driver = %{version}-%{release}

%description driver-hash
HASH driver for DSPAM.

%description driver-hash -l pl.UTF-8
Sterownik HASH dla DSPAM-a.

%package driver-mysql
Summary:	MySQL driver for DSPAM
Summary(pl.UTF-8):	Sterownik MySQL dla DSPAM-a
Group:		Libraries
Requires(post):	sed >= 4.0
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-driver = %{version}-%{release}

%description driver-mysql
MySQL driver for DSPAM.

%description driver-mysql -l pl.UTF-8
Sterownik MySQL dla DSPAM-a.

%package driver-pgsql
Summary:	PostgreSQL driver for DSPAM
Summary(pl.UTF-8):	Sterownik PostgreSQL dla DSPAM-a
Group:		Libraries
Requires(post):	sed >= 4.0
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-driver = %{version}-%{release}

%description driver-pgsql
PostgreSQL driver for DSPAM.

%description driver-pgsql -l pl.UTF-8
Sterownik PostgreSQL dla DSPAM-a.

%package driver-sqlite3
Summary:	SQLite driver for DSPAM
Summary(pl.UTF-8):	Sterownik SQLite dla DSPAM-a
Group:		Libraries
Requires(post):	sed >= 4.0
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-driver = %{version}-%{release}
Obsoletes:	dspam-driver-sqlite

%description driver-sqlite3
SQLite driver for DSPAM.

%description driver-sqlite3 -l pl.UTF-8
Sterownik SQLite dla DSPAM-a.

%package webui
Summary:	DSPAM Web UI
Summary(pl.UTF-8):	Interfejs WWW do programu DSPAM
Group:		Applications/WWW
Requires:	webapps
# needs dspam binary
Requires:	%{name} = %{version}-%{release}

%description webui
The Web UI (CGI client) can be run from any executable location on a
web server, and detects its user's identity from the REMOTE_USER
environment variable. This means you'll need to use HTTP password
authentication to access the CGI (Any type of authentication will
work, so long as Apache supports the module). This is also convenient
in that you can set up authentication using almost any existing system
you have. The only catch is that you'll need the usernames to match
the actual DSPAM usernames used the system. A copy of the shadow
password file will suffice for most common installs.

%description webui -l pl.UTF-8
Interfejs użytkownika WWW (klient CGI) może być uruchamiany z
dowolnego wykonywalnego miejsca na serwerze WWW i rozpoznaje tożsamość
użytkownika ze zmiennej środowiskowej REMOTE_USER. Oznacza to, że
trzeba użyć uwietrzytelnienia HTTP z hasłem do dostępu do CGI (działać
będzie dowolny rodzaj uwierzytelnienia obsługiwany przez moduły
Apache'a). Jest to o tyle wygodne, że można skonfigurować
uwierzytelnianie dla prawie każdego istniejącego systemu. Jedynym
wymogiem jest, żeby nazwy użytkowników pokrywały się z nazwami
użytkowników DSPAM-a używanymi w systemie. Kopia pliku shadow
wystarczy dla większości popularnych instalacji.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
sed -i -e 's#\-static##g' src/Makefile* src/*/Makefile*
%{?with_mysql40:sed -i -e 's#40100#99999#g' src/mysql_drv.c}
sed -i -e 's,/usr/local/dspam/bin,/usr/bin,' ./scripts/train.pl

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}

DRIVERS="
hash_drv
%{?with_mysql:mysql_drv}
%{?with_pgsql:pgsql_drv}
%{?with_sqlite:sqlite3_drv}
"
%configure \
	--disable-dependency-tracking \
	%{?debug: --enable-debug --enable-bnr-debug --enable-verbose-debug} \
	--enable-trusted-user-security \
	--enable-large-scale \
	--with-dspam-home=/var/lib/%{name} \
	--with-dspam-home-owner=none \
	--with-dspam-home-group=none \
	--with-dspam-owner=none \
	--with-dspam-group=none \
	--enable-ldap \
	--enable-clamav \
	--enable-preferences-extension \
	--enable-long-usernames \
	--enable-virtual-users \
	--with-storage-driver=$(echo $DRIVERS | tr ' ' ',') \
%if %{with mysql}
	--with-mysql-includes=%{_includedir}/mysql \
	--with-mysql-libraries=%{_libdir} \
%endif
%if %{with pgsql}
	--with-pgsql-includes=%{_includedir}/postgresql \
	--with-pgsql-libraries=%{_libdir} \
%endif
%if 0
%if %{with sqlite}
	--with-sqlite-includes=%{_includedir} \
	--with-sqlite-libraries=%{_libdir} \
%endif
%endif
	--enable-daemon

# --enable-dclassify-extension needs libdclassify

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/run/dspam,/etc/{rc.d/init.d,sysconfig}} \
	$RPM_BUILD_ROOT/var/lib/%{name}/{txt,data}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dspam

cp -a txt/*.txt $RPM_BUILD_ROOT/var/lib/%{name}/txt

# install devel files
install -d $RPM_BUILD_ROOT{%{_includedir}/%{name},/var/{log,lib}/%{name}}
install src/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}

# provide maintenance scripts
install -d $RPM_BUILD_ROOT/etc/cron.{daily,weekly}
cat > $RPM_BUILD_ROOT/etc/cron.daily/%{name} <<EOF
#!/bin/sh
exec %{_bindir}/%{name}_clean -s -p
EOF

chmod 755 $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/%{name}

# fix purge stuff
#install dspam-cron.weekly $RPM_BUILD_ROOT%{_sysconfdir}/cron.weekly/%{name}

%if %{with mysql}
cat > $RPM_BUILD_ROOT/var/lib/%{name}/mysql.data <<EOF
_UNCONFIGURED_

Note!

This file can only contain 5 lines with the following values:

HOSTNAME
PORT
USERNAME
PASSWORD
DATABASE
EOF
%endif

%if %{with pgsql}
cat > $RPM_BUILD_ROOT/var/lib/%{name}/pgsql.data <<EOF
_UNCONFIGURED_

Note!

This file can only contain 5 lines with the following values:

HOSTNAME
PORT
USERNAME
PASSWORD
DATABASE
EOF
%endif

install -d $RPM_BUILD_ROOT%{_webapps}/%{_webapp}
install %{SOURCE2} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/apache.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/httpd.conf
touch $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/htpasswd

%post
/sbin/chkconfig --add dspam
%service dspam restart "dspam daemon"

%preun
if [ "$1" = "0" ]; then
	%service dspam stop
	/sbin/chkconfig --del dspam
fi

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post driver-hash
%{__sed} -i -e '/^StorageDriver/s,/.*\.so,%{_libdir}/libhash_drv.so,' /etc/dspam.conf

%post driver-mysql
%{__sed} -i -e '/^StorageDriver/s,/.*\.so,%{_libdir}/libmysql_drv.so,' /etc/dspam.conf

%post driver-pgsql
%{__sed} -i -e '/^StorageDriver/s,/.*\.so,%{_libdir}/libpgsql_drv.so,' /etc/dspam.conf

%post driver-sqlite3
%{__sed} -i -e '/^StorageDriver/s,/.*\.so,%{_libdir}/libsqlite3_drv.so,' /etc/dspam.conf

%triggerin webui -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun webui -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin webui -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun webui -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README CHANGELOG RELEASE.NOTES UPGRADING
%doc doc/{courier,exim,markov,pop3filter,postfix,qmail,relay,sendmail}.txt
%doc scripts/train.pl
%dir %attr(775,root,mail) /var/run/dspam
%dir %attr(750,root,mail) /var/lib/%{name}
%dir %attr(770,root,mail) /var/lib/%{name}/data
%dir /var/lib/%{name}/txt
%config(noreplace) %verify(not md5 mtime size) /var/lib/%{name}/txt/*.txt
%dir %attr(770,root,mail) /var/log/dspam
%attr(754,root,root) /etc/rc.d/init.d/dspam
%attr(755,root,root) %config(noreplace) /etc/cron.daily/%{name}
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}_logrotate
%attr(755,root,root) %{_bindir}/%{name}_clean
%attr(755,root,root) %{_bindir}/%{name}_crc
%attr(755,root,root) %{_bindir}/%{name}_dump
%attr(755,root,root) %{_bindir}/%{name}_stats
%attr(755,root,root) %{_bindir}/%{name}_merge
%attr(755,root,root) %{_bindir}/%{name}_2sql
%attr(755,root,root) %{_bindir}/%{name}_admin
%attr(755,root,root) %{_bindir}/%{name}_train
%{_mandir}/man?/%{name}*

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}c

%files common
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dspam.conf

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdspam.so.7.0.0
%attr(755,root,root) %ghost %{_libdir}/libdspam.so.7

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdspam.so
%attr(755,root,root) %{_libdir}/lib*_drv.so
%{_libdir}/libdspam.la
%{_libdir}/lib*_drv.la
%{_includedir}/%{name}
%{_mandir}/man3/libdspam.3*
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libdspam.a
%{_libdir}/lib*_drv.a

%files driver-hash
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/css*
%attr(755,root,root) %{_libdir}/libhash_drv.so.7.0.0
%attr(755,root,root) %ghost %{_libdir}/libhash_drv.so.7

%if %{with mysql}
%files driver-mysql
%defattr(644,root,root,755)
%doc doc/mysql_drv.txt src/tools.mysql_drv/*.sql
%attr(640,root,mail) %config(noreplace) /var/lib/%{name}/mysql.data
%attr(755,root,root) %{_libdir}/libmysql_drv.so.7.0.0
%attr(755,root,root) %ghost %{_libdir}/libmysql_drv.so.7
%endif

%if %{with pgsql}
%files driver-pgsql
%defattr(644,root,root,755)
%doc doc/pgsql_drv.txt src/tools.pgsql_drv/*.sql
%attr(640,root,mail) %config(noreplace) /var/lib/%{name}/pgsql.data
%attr(755,root,root) %{_bindir}/%{name}_pg2int8
%attr(755,root,root) %{_libdir}/libpgsql_drv.so.7.0.0
%attr(755,root,root) %ghost %{_libdir}/libpgsql_drv.so.7
%endif

%if %{with sqlite}
%files driver-sqlite3
%defattr(644,root,root,755)
%doc doc/sqlite_drv.txt
%attr(755,root,root) %{_libdir}/libsqlite3_drv.so.7.0.0
%attr(755,root,root) %ghost %{_libdir}/libsqlite3_drv.so.7
%endif

%files webui
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_webapps}/%{_webapp}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/htpasswd
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/admins
%attr(660,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/default.prefs
%config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/configure.pl

%dir %{_datadir}/dspam
%dir %{_datadir}/dspam/cgi
%attr(755,root,root) %{_datadir}/dspam/cgi/*.cgi
%{_datadir}/dspam/cgi/templates
%{_datadir}/dspam/htdocs
