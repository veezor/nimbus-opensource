Name:           NimbusClientService
Version:        1.1
Release:        68.1
License:        GPL v2
Summary:        Nimbus Client for Nimbus Cloud Backup
Url:            http://www.nimbusbackup.com
Group:          Development/Libraries/Python
Source:         nimbus-client.tar.gz
BuildRequires:  python python-setuptools redhat-rpm-config
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts

 
%description
Nimbus client for Nimbus Cloud Backup


%prep
%setup -q -n client


%post
if [ "$1" -ge "1" ] ; then
    /sbin/chkconfig --level 345 nimbusclient on >/dev/null 2>&1 || :
    /sbin/service nimbusclient start >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service nimbusclient stop >/dev/null 2>&1 || :
    /sbin/chkconfig --level 345 nimbusclient off >/dev/null 2>&1 || :
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service nimbusclient condrestart >/dev/null 2>&1 || :
fi

 
%build
%{__python} setup.py build
 
 
%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot} 
 
 
%files 
%defattr(-,root,root)
/etc/init.d/nimbusclient
/usr/bin/nimbusclientservice
/usr/bin/nimbusnotifier
/etc/nimbus
