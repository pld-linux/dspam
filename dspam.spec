Summary:	A library and Mail Delivery Agent for Bayesian spam filtering
Name:		dspam
Version:	2.10.6
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	http://www.nuclearelephant.com/projects/dspam/sources/%{name}-%{version}.tar.gz
URL:		http://www.nuclearelephant.com/projects/dspam/
BuildRequires:	mysql-devel
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DSPAM (as in De-Spam) is an open-source project to create a new kind
of anti-spam mechanism, and is currently effective as both a
server-side agent for UNIX email servers and a developer's library for
mail clients, other anti-spam tools, and similar projects requiring
drop-in spam filtering.

The DSPAM agent masquerades as the email server's local delivery agent
and filters/learns spams using an advanced Bayesian statistical
approach (based on Baye's theorem of combined probabilities) which
provides an administratively maintenance-free, easy-learning Anti-Spam
service custom tailored to each individual user's behavior. Advanced
because on top of standard Bayesian filtering is also incorporated the
use of Chained Tokens, de-obfuscation, and other enhancements. DSPAM
works great with Sendmail and Exim, and should work well with any
other MTA that supports an external local delivery agent (postfix,
qmail, etc.)

%package libs
Summary:	A library and Mail Delivery Agent for Bayesian spam filtering
Group:		Libraries

%description libs
DSPAM (as in De-Spam) is an open-source project to create a new kind
of anti-spam mechanism, and is currently effective as both a
server-side agent for UNIX email servers and a developer's library for
mail clients, other anti-spam tools, and similar projects requiring
drop-in spam filtering.

The DSPAM agent masquerades as the email server's local delivery agent
and filters/learns spams using an advanced Bayesian statistical
approach (based on Baye's theorem of combined probabilities) which
provides an administratively maintenance-free, easy-learning Anti-Spam
service custom tailored to each individual user's behavior. Advanced
because on top of standard Bayesian filtering is also incorporated the
use of Chained Tokens, de-obfuscation, and other enhancements. DSPAM
works great with Sendmail and Exim, and should work well with any
other MTA that supports an external local delivery agent (postfix,
qmail, etc.)

%package devel
Summary:	Development library and header files for the %{name} library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
DSPAM has had its core engine moved into a separate library, libdspam.
This library can be used by developers to provide 'drop-in' spam
filtering for their mail client applications, other anti-spam tools,
or similar projects.

%prep
%setup -q

%build
%configure2_13 \
    --enable-trusted-user-security \
    --enable-bayesian-dobly \
    --enable-chained-tokens \
    --enable-neural-networking \
    --enable-experimental \
    --enable-signature-attachments \
    --enable-bias \
    --enable-large-scale \
    --enable-delivery-to-stdout \
    --enable-virtual-users \
    --with-userdir=/var/lib/%{name} \
    --with-userdir-owner=none \
    --with-userdir-group=none \
    --with-dspam-owner=none \
    --with-dspam-group=none \
    --with-signature-life=14 \
    --disable-dependency-tracking \
    --enable-virtual-users \
    --with-storage-driver=mysql_drv \
    --with-mysql-includes=%{_includedir}/mysql \
    --with-mysql-libraries=%{_libdir}/mysql \
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

# install devel files
install -d %{buildroot}%{_includedir}/%{name}
install -m0644 libdspam.h %{buildroot}%{_includedir}/%{name}/
install -m0644 libdspam_objects.h %{buildroot}%{_includedir}/%{name}/
install -m0644 lht.h %{buildroot}%{_includedir}/%{name}/
install -m0644 nodetree.h %{buildroot}%{_includedir}/%{name}/

# provide maintenance scripts
install -d %{buildroot}%{_sysconfdir}/cron.daily
install -d %{buildroot}%{_sysconfdir}/cron.weekly

cat > %{buildroot}%{_sysconfdir}/cron.daily/%{name} <<EOF
#!/bin/sh
exec %{_bindir}/%{name}_clean 2>&1 > /dev/null
EOF

chmod 755 %{buildroot}%{_sysconfdir}/cron.daily/%{name}

# fix prefix
perl -pi -e "s|%{_prefix}/local|%{_prefix}|g" %{buildroot}%{_bindir}/%{name}_corpus
perl -pi -e "s|%{_prefix}/local|%{_prefix}|g" cgi/dspam.cgi

cp tools.mysql_drv/README README.mysql

# fix purge stuff
install -m0755 dspam-cron.weekly %{buildroot}%{_sysconfdir}/cron.weekly/%{name}

# fix missing file
install -d %{buildroot}/var/lib/%{name}
cat > %{buildroot}/var/lib/%{name}/mysql.data <<EOF
_UNCONFIGURED_

Note!

This file can only contain 5 lines with the following values:

HOSTNAME
PORT
USERNAME
PASSWORD
DATABASE
EOF

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc README CHANGE
%doc cgi/base.css cgi/dspam.cgi cgi/logo.gif cgi/template.html
%doc README.mysql
%doc tools.mysql_drv/mysql_objects.sql.space.optimized
%doc tools.mysql_drv/mysql_objects.sql.speed.optimized
%doc tools.mysql_drv/purge.sql
%doc tools.mysql_drv/virtual_users.sql
%dir %attr(0750,root,mail) /var/lib/%{name}
%attr(0640,root,mail) %config(noreplace) /var/lib/%{name}/mysql.data
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cron.daily/%{name}
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cron.weekly/%{name}
%attr(0755,root,mail) %{_bindir}/%{name}
%attr(0755,root,root) %{_bindir}/%{name}_clean
%attr(0755,root,root) %{_bindir}/%{name}_corpus
%attr(0755,root,root) %{_bindir}/%{name}_crc
%attr(0755,root,root) %{_bindir}/%{name}_dump
%attr(0755,root,root) %{_bindir}/%{name}_genaliases
%attr(0755,root,root) %{_bindir}/%{name}_stats
%attr(0755,root,root) %{_bindir}/%{name}_merge
%attr(0755,root,root) %{_bindir}/%{name}_2mysql
%attr(0755,root,root) %{_bindir}/%{name}_ngstats

%files libs
%defattr(644,root,root,755)
%doc README CHANGE
%attr(0755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%attr(0644,root,root) %{_includedir}/%{name}/*.h
%attr(0755,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/*.la
%attr(0755,root,root) %{_libdir}/*.a
